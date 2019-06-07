#!/usr/bin/env python
import shared

from actions import Action_Factory
from constants import *
from outputs import print_tasks
from utils import *


def _get_string(stdscr):
    stdscr.nodelay(0)
    read_str = stdscr.getstr()
    stdscr.nodelay(1)
    return read_str

def _handle(stdscr, action, task_list, y, max_x):
    current = task_list.get_selected()

    if action in STRING_ACTIONS:
        read_str = _get_string(stdscr)
        read_str = read_str.decode('utf-8')
        Action_Factory.do_action(action, current, read_str)
    else:
        Action_Factory.do_action(action, current)
    
    task_list.to_yaml(TASK_PATH)

def accept_input(stdscr, task_line):
    max_y, max_x = stdscr.getmaxyx()
    global CONTINUE

    while True:
        next_line, task_list = print_tasks(stdscr, task_line, max_x)
        read_char = stdscr.getch()
        try:
            _handle(stdscr, chr(read_char), task_list, task_line, max_x)
            next_line, task_list = print_tasks(stdscr, task_line, max_x)
            clear(stdscr, next_line-1, max_y - len(CLOCK[0]), max_x)
        except ValueError:
            pass
        except CleanExit:
            with shared.quit_lock:
                shared.is_quit = True
            break
