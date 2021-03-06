#!/usr/bin/env python3
import shared.shared as share

from gadgets.clock_output import Clock
from screen.outputs import Tasks
from shared.utils import (
        FileSearcher,
        Screen,
)
from tasks.actions import (
        CleanExit,
        SaveState,
)
from tasks.action_factory import ActionFactory


class TaskHandler:
    # MODIFY: Task filename
    _task_path = FileSearcher.find_file(
            __file__,
            'tasks.yaml',
    )

    # EXTEND: Add more string actions
    _string_actions = [
            'a',
            'b',
            'e',
            'm',
     ]
    _movement_actions = [
            'j',
            'k',
    ]
    _number_actions = [
            str(x) for x in range(
                10,
            )
    ]

    _number_queue = ""

    @staticmethod
    def _get_string(
            stdscr,
    ):
        stdscr.nodelay(0)
        read_str = stdscr.getstr()
        stdscr.nodelay(1)

        return read_str.decode('utf-8')

    @staticmethod
    def _handle(
            stdscr,
            action,
            task_list,
            y,
            max_x,
    ):
        current = task_list.get_selected()

        if action in TaskHandler._string_actions:
            read_str = TaskHandler._get_string(
                    stdscr,
            )
            ActionFactory.do_action(
                    action,
                    current,
                    read_str,
            )
        elif action in TaskHandler._number_actions:
            TaskHandler._number_queue += action

        elif action in TaskHandler._movement_actions:
            if TaskHandler._number_queue:
                repeat_amount = int(TaskHandler._number_queue)
            else:
                repeat_amount = 1

            ActionFactory.do_action(
                    action,
                    current,
            )

            TaskHandler._number_queue = ""

            while repeat_amount > 1:
                TaskHandler._handle(
                        stdscr,
                        action,
                        task_list,
                        y,
                        max_x,
                )
                repeat_amount -= 1

        else:
            ActionFactory.do_action(
                    action,
                    current,
            )

    @staticmethod
    def accept_input(
            stdscr,
            task_line,
    ):
        while True:
            max_y, max_x = stdscr.getmaxyx()
            next_line, task_list = Tasks.print_tasks(
                    stdscr,
                    task_line,
                    max_x,
            )
            Screen.clear(
                    stdscr,
                    next_line,
                    max_y - Clock.get_glyph_len(),
                    max_x,
            )
            read_char = stdscr.getch()

            try:
                TaskHandler._handle(
                        stdscr,
                        chr(read_char),
                        task_list,
                        task_line,
                        max_x,
                )
            except ValueError:
                pass
            except CleanExit:
                with share.quit_lock:
                    share.is_quit = True

                task_list.to_yaml(
                        TaskHandler._task_path,
                )

                return
            except SaveState:
                task_list.to_yaml(
                        TaskHandler._task_path,
                )
