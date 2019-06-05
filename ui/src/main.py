#!/usr/bin/env pxthon3
import curses
import datetime
import uuid
import yaml

from actions import Action_Factory
from constants import *
from tasks import Task_List
from time import sleep
from threading import Thread

BANNER_PATH = 'ui/files/banner'
TASK_PATH = 'ui/files/tasks.yaml'


class GlyphError(Exception):
    pass


def setup_colors():
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

def _combine_glyphs(orig, to_add):
    if len(orig) != len(to_add):
        raise GlyphError('Glyph Lengths are not equal')
    
    for i, g in enumerate(to_add):
        orig[i] += g

def _val_to_glyph(num):
    digits = []

    if num >= 10:
        digits.append(num // 10)
        num %= 10
    digits.append(num)

    glyphs = [''] * GLYPH_LEN
    for digit in digits:
        glyph = CLOCK[digit]
        _combine_glyphs(glyphs, glyph)

    return glyphs

def _get_time():
    time_str = str(datetime.datetime.now().time())
    return time_str.split(':')[:2]

def _determine_clock():
    hours, minutes = _get_time()
    hours, minutes = int(hours), int(minutes)

    # Default
    color = COLOR_PAIR['GOOD']

    # After Hours, Go Home!
    if hours < 9 or hours > 18:
        color = COLOR_PAIR['ERROR']

    # TODO: Add Meeting Now / Meeting Soon
    
    return color

def print_clock(stdscr, y, x):
    clock_color = _determine_clock()
    hours, minutes = _get_time()

    hour = int(hours) % 12
    if hour == 0:
        hour = 12
    time_glyphs = _val_to_glyph(hour)

    _combine_glyphs(time_glyphs, CLOCK[':'])
    
    minute = int(minutes) % 60
    if minute < 10:
        _combine_glyphs(time_glyphs, CLOCK[0])
    _combine_glyphs(time_glyphs, _val_to_glyph(minute))

    x //= 2
    x -= (len(time_glyphs[0]) - 1) // 2
    for minus, line in enumerate(reversed(time_glyphs), 1):
        stdscr.addstr(y - minus, x, line, clock_color)

    return y

def clean(stdscr, x_start, x_end, y_start, y_end):
    for y in range(y_start, y_end):
        stdscr.addstr(y, x_start, ' ' * (x_end - x_start - 1), COLOR_PAIR['TEXT'])

def update_clock(stdscr):
    while True:
        max_y, max_x = stdscr.getmaxyx()
        clean(stdscr, 0, max_x, max_y - GLYPH_LEN, max_y)
        print_clock(stdscr, max_y, max_x)
        sleep(10)

def print_banner(stdscr, y, x):
    with open(BANNER_PATH, 'r') as f:
        banner = f.read()

    for y, line in enumerate(banner.splitlines(), y):
        stdscr.addstr(y, x, line, COLOR_PAIR['BOLD'])

    return y

def _get_color(task):
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
    

def print_tasks(stdscr, y, max_x):
    task_list = Task_List.from_yaml(TASK_PATH)

    for y, task in enumerate(task_list, y):
        task_str = str(task)
        if task_str:
            task_attr = _get_color(task)
            stdscr.addstr(y, 0, task_str + ' ' * (max_x - len(task_str)),
                    task_attr)

    return y, task_list

def handle(stdscr, action, task_list, y, max_x):
    current = task_list.get_selected()

    if action in STRING_ACTIONS:
        read_str = get_string(stdscr)
        read_str = read_str.decode('utf-8')
        Action_Factory.do_action(action, current, read_str)
    else:
        Action_Factory.do_action(action, current)
    
    task_list.to_yaml(TASK_PATH)

def get_string(stdscr):
    stdscr.nodelay(0)
    read_str = stdscr.getstr()
    stdscr.nodelay(1)
    return read_str

def clear(stdscr, top, bottom, max_x):
    for y in range(top + 1, bottom):
        stdscr.addstr(y, 0, ' ' * max_x, COLOR_PAIR['TEXT'])

def accept_input(stdscr, task_list, task_line):
    max_y, max_x = stdscr.getmaxyx()


    while True:
        next_line, task_list = print_tasks(stdscr, task_line, max_x)
        read_char = stdscr.getch()
        try:
            handle(stdscr, chr(read_char), task_list, task_line, max_x)
            next_line, task_list = print_tasks(stdscr, task_line, max_x)
            clear(stdscr, next_line-1, max_y - len(CLOCK[0]), max_x)
        except ValueError as e:
            pass

def main(stdscr):
    stdscr.nodelay(1)
    setup_colors()

    max_y, max_x = stdscr.getmaxyx()

    # Give line space
    task_line = print_banner(stdscr, 0, 0) + 2

    next_line, task_list = print_tasks(stdscr, task_line, max_x)

    thread = Thread(target=update_clock, args=(stdscr,))
    thread.start()

    accept_input(stdscr, task_list, task_line)

if __name__ == '__main__':
    curses.wrapper(main)
