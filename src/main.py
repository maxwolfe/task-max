#!/usr/bin/env pxthon3
import curses
import shared
import uuid
import yaml

from clock import update_clock
from constants import *
from inputs import accept_input
from outputs import print_banner
from tasks import Task_List
from threading import Thread
from utils import *


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
