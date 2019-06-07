#!/usr/bin/env python
from shared.color import get_color, COLOR_PAIR
from shared.constants import *
from shared.utils import *
from tasks.tasks import Task_List


def print_banner(stdscr, y, x):
    with open(BANNER_PATH, 'r') as f:
        banner = f.read()

    for y, line in enumerate(banner.splitlines(), y):
        stdscr.addstr(y, x, line, COLOR_PAIR['BOLD'])

    return y

def print_tasks(stdscr, y, max_x):
    task_list = Task_List.from_yaml(TASK_PATH)

    for y, task in enumerate(task_list, y):
        task_str = str(task)
        if task_str:
            task_attr = get_color(task)
            stdscr.addstr(y, 0, task_str + ' ' * (max_x - len(task_str)),
                    task_attr)

    return y, task_list
