#!/usr/bin/env python3
import shared.shared as share

from time import sleep

from colors.color import Colors
from gadgets.line_numbers import LineNumbers
from shared.utils import FileSearcher
from tasks.task_list import TaskList


class Banner:
    _banner = None

    # MODIFY: Defaults
    _default_color = 'Bold'
    _banner_path = FileSearcher.find_file(
            __file__,
            'banner',
    )

    @staticmethod
    def _load_banner():
        if not Banner._banner:
            with open(Banner._banner_path, 'r') as f:
                Banner._banner = f.read()

        return Banner._banner

    @staticmethod
    def _print_banner(
            stdscr,
            y,
            x,
    ):
        banner = Banner._load_banner()

        for y, line in enumerate(
                banner.splitlines(),
                y,
        ):
            stdscr.addstr(
                    y,
                    x,
                    line,
                    Colors.get_color(Banner._default_color)
            )

        return y

    @staticmethod
    def loop_banner(
            stdscr,
            y,
            x,
    ):
        while True:
            with share.quit_lock:
                if share.is_quit:
                    break
            Banner._print_banner(
                    stdscr,
                    y,
                    x,
            )
            sleep(1)

    @staticmethod
    def banner_lines():
        banner = Banner._load_banner()

        return banner.count('\n')


class Tasks:
    _task_list = None

    # MODIFY: Task filename
    _task_path = FileSearcher.find_file(
            __file__,
            'tasks.yaml',
    )

    @staticmethod
    def _load_task_list():
        if not Tasks._task_list:
            Tasks._task_list = TaskList.from_yaml(Tasks._task_path)

        return Tasks._task_list

    @staticmethod
    def print_tasks(
            stdscr,
            y,
            max_x,
    ):
        task_list = Tasks._load_task_list()

        selected = 0
        start_y = y

        for y, task in enumerate(
                task_list,
                y,
        ):
            task_str = str(task)

            if task.selected:
                selected = y - start_y

            if task_str:
                task_attr = Colors.get_color(
                        task.color,
                )
                stdscr.addstr(
                        y,
                        4,
                        task_str + ' ' * (max_x - len(task_str) - 4),
                        task_attr,
                )

        LineNumbers.update_line_nums(
                stdscr,
                start_y,
                y,
                selected,
        )

        return y, task_list
