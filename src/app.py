#!/usr/bin/env python3
import curses

from time import sleep
from threading import Thread

from gadgets.clock_output import update_clock
from screen.inputs import accept_input
from screen.outputs import print_banner, loop_banner
from screen.resize import resize
from shared.utils import *




def main(stdscr):
    stdscr.nodelay(1)

    max_y, max_x = stdscr.getmaxyx()

    # Give line space
    task_line = print_banner(stdscr, 0, 0) + 2

    actions = [
            (
                loop_banner, 
                (
                    stdscr,
                    0,
                    0,
                ),
            ),
            (
                resize,
                (
                    stdscr,
                    max_y,
                    max_x,
                ),
            ),
            (
                update_clock,
                (
                    stdscr,
                )
            ),
            (
                accept_input,
                (
                    stdscr,
                    task_line,
                ),
            ),
    ]


    thread_list = []

    for targ, arg in actions:
        thread = Thread(
                target=targ,
                args=arg,
        )
        thread.start()
        thread_list.append(thread)

    for thread in thread_list:
        thread.join()

if __name__ == '__main__':
    curses.wrapper(main)
