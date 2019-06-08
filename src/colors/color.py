#!/usr/bin/env python
import curses
import json
import yaml

from shared.constants import *

COLOR_PAIR = {'Highlight': curses.A_STANDOUT,
              'Blink': curses.A_BLINK,
              'Bold': curses.A_BOLD,
              'Dim': curses.A_DIM,
              'Line': curses.A_UNDERLINE,
             }

COUNTER = 0
SELECT = -1


def _load_color(str_key, byte_key, bg):
    global COUNTER

    try:
        curses.init_pair(COUNTER, byte_key, bg)
        COLOR_PAIR[str_key] = curses.color_pair(COUNTER)
        COUNTER += 1
    except curses.error:
        #TODO: Maximum number of pairs reached?
        pass
   
def _load_colors_from_dict(color_dict):
    for key in color_dict:
        color_entry = color_dict[key]
        str_key = color_entry.get('name')
        byte_key = color_entry.get('colorId')
        bg = color_entry.get('bg', -1)
        if str_key and byte_key:
            _load_color(str_key, byte_key, bg)
            if bg != SELECT:
                _load_color('Select_{}'.format(str_key),
                            byte_key,
                            SELECT,
                           )

def _load_xterm_colors():
    try:
        with open(XTERM_PATH, 'r') as f:
            color_list = json.loads(f.read())
    except FileNotFoundError:
        color_list = []

    color_dict = {}
    for key, data in enumerate(color_list):
        color_dict[key] = data

    _load_colors_from_dict(color_dict)

def _load_custom_colors():
    global SELECT

    try:
        with open(CUSTOM_COLOR_PATH, 'r') as f:
            color_dict = yaml.safe_load(f.read())
    except FileNotFoundError:
        color_dict = {}

    if 'Select' in color_dict.keys():
       SELECT = color_dict['Select'].get('select_id', SELECT)
       del color_dict['Select']

    _load_colors_from_dict(color_dict)
    
def _setup_colors():
    curses.start_color()
    curses.use_default_colors()

    _load_custom_colors()
    _load_xterm_colors()

def get_color(color):
    return COLOR_PAIR.get(color, COLOR_PAIR['White'])

# Run on import
_setup_colors()
