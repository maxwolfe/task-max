#!/usr/bin/env python3
import shared.shared as share

from time import sleep

from colors.color import Colors
from shared.utils import FileSearcher
from tasks.tasks import Task_List


class Banner:
    _banner_path = FileSearcher.find_file(
            __file__,
            'banner',
    )
    _banner = None
    _default_color = 'Bold'

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
    _task_path = FileSearcher.find_file(
            __file__,
            'tasks.yaml',
    )
    _task_list = None

    @staticmethod
    def _load_task_list():
        if not Tasks._task_list:
            Tasks._task_list = Task_List.from_yaml(Tasks._task_path)

        return Tasks._task_list

    @staticmethod
    def print_tasks(
            stdscr,
            y,
            max_x,
    ):
        task_list = Tasks._load_task_list()

        for y, task in enumerate(
                task_list,
                y,
        ):
            task_str = str(task)

            if task_str:
                task_attr = Colors.get_color(
                        task.color,
                )
                stdscr.addstr(
                        y,
                        0,
                        task_str + ' ' * (max_x - len(task_str)),
                        task_attr,
                )

        return y, task_list
