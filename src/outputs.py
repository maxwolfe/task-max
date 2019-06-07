#!/usr/bin/env python
from color import get_color, COLOR_PAIR
from constants import *
from tasks import Task_List
from utils import *


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
