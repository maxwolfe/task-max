#!/usr/bin/env python
from color import COLOR_PAIR
from constants import *


def clean(stdscr, x_start, x_end, y_start, y_end):
    for y in range(y_start, y_end):
        stdscr.addstr(y, x_start, ' ' * (x_end - x_start - 1), COLOR_PAIR['TEXT'])

def clear(stdscr, top, bottom, max_x):
    for y in range(top + 1, bottom):
        stdscr.addstr(y, 0, ' ' * max_x, COLOR_PAIR['TEXT'])
