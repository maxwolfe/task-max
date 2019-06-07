#!/usr/bin/env python
import shared

from constants import *
from datetime import datetime
from time import sleep
from utils import *


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
    time_str = str(datetime.now().time())
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

def _print_clock(stdscr, y, x):
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

def update_clock(stdscr):
    while True:
        with shared.quit_lock:
            if shared.is_quit:
                break
        max_y, max_x = stdscr.getmaxyx()
        clean(stdscr, 0, max_x, max_y - GLYPH_LEN, max_y)
        _print_clock(stdscr, max_y, max_x)
        sleep(1)
