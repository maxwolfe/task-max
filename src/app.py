#!/usr/bin/env python3
import curses
import shared
import uuid
import yaml

from threading import Thread

from gadgets.clock_output import update_clock
from screen.inputs import accept_input
from screen.outputs import print_banner
from shared.constants import *
from shared.utils import *
from tasks.tasks import Task_List


def main(stdscr):
    stdscr.nodelay(1)

    max_y, max_x = stdscr.getmaxyx()

    # Give line space
    task_line = print_banner(stdscr, 0, 0) + 2

    thread = Thread(target=update_clock, args=(stdscr,))
    thread.start()

    accept_input(stdscr, task_line)
    thread.join()

if __name__ == '__main__':
    curses.wrapper(main)
