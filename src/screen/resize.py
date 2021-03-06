#!/usr/bin/env python
import curses
import shared.shared as share

from time import sleep


def resize(
        stdscr,
        y,
        x,
):
    while True:
        with share.quit_lock:
            if share.is_quit:
                return

        if curses.is_term_resized(y, x):
            y, x = stdscr.getmaxyx()
            stdscr.clear()
            curses.resizeterm(y, x)
            stdscr.refresh()

        sleep(1)
