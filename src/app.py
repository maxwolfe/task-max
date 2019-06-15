#!/usr/bin/env python3
import curses

from threading import Thread

from gadgets.clock_output import Clock
from screen.inputs import TaskHandler
from screen.outputs import Banner
from screen.resize import resize


def main(stdscr):
    stdscr.nodelay(1)

    max_y, max_x = stdscr.getmaxyx()

    # Give line space
    task_line = Banner.banner_lines() + 1

    actions = [
            (
                Banner.loop_banner,
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
                Clock.update_clock,
                (
                    stdscr,
                )
            ),
            (
                TaskHandler.accept_input,
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
