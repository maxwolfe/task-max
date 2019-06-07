#!/usr/bin/env python
import curses

from shared.constants import *

COLOR_PAIR = defaultdict(lambda: curses.color_pair(1))
SETUP = True


def _setup_colors():
    curses.start_color()
    curses.use_default_colors()

    for key in USE_COLOR:
        num, fg, bg = USE_COLOR[key]
        curses.init_pair(num, fg, bg)
        COLOR_PAIR[key] = curses.color_pair(num)

    for key in LEVEL:
        num, fg, bg = LEVEL[key]
        curses.init_pair(num, fg, bg)
        COLOR_PAIR[key] = curses.color_pair(num)

    COLOR_PAIR['HIGHLIGHT'] = curses.A_STANDOUT
    COLOR_PAIR['BLINK'] = curses.A_BLINK
    COLOR_PAIR['BOLD'] = curses.A_BOLD
    COLOR_PAIR['DIM'] = curses.A_DIM
    COLOR_PAIR['LINE'] = curses.A_UNDERLINE


def get_color(task):
    global SETUP

    if SETUP:
        _setup_colors()
        SETUP = False

    if task.priority == 0:
        if task.selected:
            return COLOR_PAIR['SELECT_EPIC']
        elif task.blocked:
            return COLOR_PAIR['BLOCKED_EPIC']
        return COLOR_PAIR['EPIC']
    elif task.priority == 1:
        if task.selected:
            return COLOR_PAIR['SELECT_SPRINT']
        elif task.blocked:
            return COLOR_PAIR['BLOCKED_SPRINT']
        return COLOR_PAIR['SPRINT']
    elif task.priority == 2:
        if task.selected and task.blocked:
            return COLOR_PAIR['SELECT_BLOCKER']
        elif task.selected:
            return COLOR_PAIR['SELECT_FAST']
        elif task.blocked:
            return COLOR_PAIR['BLOCKER']
        return COLOR_PAIR['BOLD']
    
    return COLOR_PAIR['TEXT']
