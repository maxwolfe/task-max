#!/usr/bin/env python3
import curses
import yaml

from collections import defaultdict

COLORS = {"BLACK" : curses.COLOR_BLACK,
          "RED" : curses.COLOR_RED,
          "GREEN": curses.COLOR_GREEN,
          "WHITE": curses.COLOR_WHITE,
          "YELLOW": curses.COLOR_YELLOW,
         }
USE_COLOR = {"TEXT": (1, COLORS["WHITE"], COLORS["BLACK"]),
             "ERROR": (2, COLORS["RED"], COLORS["BLACK"]),
             "GOOD": (3, COLORS["GREEN"], COLORS["BLACK"]),
            }
COLOR_PAIR = defaultdict(lambda: curses.color_pair(1))

BANNER_PATH = "ui/files/banner"

def setup_colors():
    for key in USE_COLOR:
        num, fg, bg = USE_COLOR[key]
        curses.init_pair(num, fg, bg)
        COLOR_PAIR[key] = curses.color_pair(num)

    COLOR_PAIR["HIGHLIGHT"] = curses.A_STANDOUT

def print_banner(stdscr):
    with open(BANNER_PATH, 'r') as f:
        banner = f.read()

    for x, line in enumerate(banner.splitlines()):
        stdscr.addstr(x, 0, line, COLOR_PAIR["TEXT"])

    return x

def print_tasks(stdscr, x, y):
    stdscr.addstr(x, y, "First Line!", COLOR_PAIR["GOOD"])
    stdscr.addstr(x + 1, y, "Bad Line!", COLOR_PAIR["BAD"])
    stdscr.addstr(x + 2, y, "Error Line!", COLOR_PAIR["ERROR"])
    stdscr.addstr(x + 3, y, "Highlight Line!", COLOR_PAIR["HIGHLIGHT"])


def main(stdscr):
    setup_colors()

    # Give line space
    next_line = print_banner(stdscr) + 2

    print_tasks(stdscr, next_line, 0)



    stdscr.getch()

if __name__ == '__main__':
    curses.wrapper(main)
