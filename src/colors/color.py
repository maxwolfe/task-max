#!/usr/bin/env python
import curses
import json
import yaml

from shared.constants import *

BG_DEFAULT = -1
SELECT_DEFAULT = 238

COLOR_PAIR = {'Highlight': curses.A_STANDOUT,
              'Blink': curses.A_BLINK,
              'Bold': curses.A_BOLD,
              'Dim': curses.A_DIM,
              'Line': curses.A_UNDERLINE,
             }

class LoadColors:
    @staticmethod
    def load():
        LoadColors._load_custom_colors()
        LoadColors._load_xterm_colors()

    @staticmethod
    def load_number():
        for num in range(1,512):
            yield num
        raise StopIteration

    @staticmethod
    def _load_color(int_key, str_key, byte_key, bg):
        curses.init_pair(int_key, byte_key, bg)
        COLOR_PAIR[str_key] = curses.color_pair(int_key)
    
    @staticmethod
    def _load_colors_from_dict(color_dict):
        for key in sorted(color_dict.keys()):
            color_entry = color_dict[key]
            str_key = color_entry.get('name')
            byte_key = color_entry.get('colorId')
            bg = color_entry.get('bg', BG_DEFAULT)
            select = color_entry.get('select', SELECT_DEFAULT)

            try:
                if str_key and byte_key:
                    LoadColors._load_color(next(LoadColors.loader), str_key, byte_key, bg)
                    if bg != select:
                        LoadColors._load_color(next(LoadColors.loader),
                                    'Select_{}'.format(str_key),
                                    byte_key,
                                    select,
                                   )
                LoadColors.last = str_key
            except StopIteration:
                # Maximum Number of Colors Loaded
                pass

    @staticmethod
    def _load_xterm_colors():
        try:
            with open(XTERM_PATH, 'r') as f:
                color_list = json.loads(f.read())
        except FileNotFoundError:
            color_list = []

        color_dict = {}
        for key, data in enumerate(color_list):
            color_dict[key] = data

        LoadColors._load_colors_from_dict(color_dict)

    @staticmethod
    def _load_custom_colors():
        LoadColors.loader = LoadColors.load_number()

        try:
            with open(CUSTOM_COLOR_PATH, 'r') as f:
                color_dict = yaml.safe_load(f.read())
        except FileNotFoundError:
            color_dict = {}

        LoadColors._load_colors_from_dict(color_dict)
    
class SetupColors:
    SETUP = True

    @staticmethod
    def setup():
        if SetupColors.SETUP:
            SetupColors._setup_colors()
            SetupColors.SETUP = False

    @staticmethod
    def _setup_colors():
        curses.start_color()
        curses.use_default_colors()

        LoadColors.load()
        print (LoadColors.last)

def get_color(color):
    SetupColors.setup()
    return COLOR_PAIR.get(color, COLOR_PAIR['White'])
