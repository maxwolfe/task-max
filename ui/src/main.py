#!/usr/bin/env pxthon3
import curses
import datetime
import yaml

from collections import defaultdict
from tasks import Epic, Sprint_Task, Fast_Task, Blocker

COLORS = {'BLACK': 0,
          'BG': -1,
          'RED': 196, 
          'GREEN': 28,
          'WHITE': 231,
          'YELLOW': 226,
          'BLUE': 39,
          'PINK': 201,
          'ORANGE': 166,
          'GREY': 242,
          'PURPLE': 129,
          'BLOCKED': -1,
          'SELECT': 238,
         }
USE_COLOR = {'TEXT': (1, COLORS['WHITE'], COLORS['BG']),
             'ERROR': (2, COLORS['RED'], COLORS['BG']),
             'GOOD': (3, COLORS['GREEN'], COLORS['BG']),
             'EPIC': (4, COLORS['PURPLE'], COLORS['BG']),
             'BLOCKED_EPIC': (5, COLORS['PURPLE'], COLORS['BLOCKED']),
             'SPRINT': (6, COLORS['BLUE'], COLORS['BG']),
             'BLOCKED_SPRINT': (7, COLORS['BLUE'], COLORS['BLOCKED']),
             'BLOCKER': (8, COLORS['RED'], COLORS['BG']),
             'SELECT_EPIC': (9, COLORS['PURPLE'], COLORS['SELECT']),
             'SELECT_SPRINT': (10, COLORS['BLUE'], COLORS['SELECT']),
             'SELECT_BLOCKER': (11, COLORS['RED'], COLORS['SELECT']),
             'SELECT_FAST': (12, COLORS['WHITE'], COLORS['SELECT']),
            }
LEVEL = {0: (len(USE_COLOR) + 1, COLORS['ORANGE'], COLORS['BG']),
         1: (len(USE_COLOR) + 2, COLORS['PURPLE'], COLORS['BG']),
         2: (len(USE_COLOR) + 3, COLORS['BLUE'], COLORS['BG']),
         3: (len(USE_COLOR) + 4, COLORS['PINK'], COLORS['BG']),
        }
COLOR_PAIR = defaultdict(lambda: curses.color_pair(1))
CLOCK = {0: ['  #####   ', ' ##   ##  ', '##     ## ', '##     ## ', '##     ## ',
	      ' ##   ##  ', '  #####   '],
         1: ['    ##    ', '  ####    ', '    ##    ', '    ##    ', '    ##    ',
	       '    ##    ', '  ######  '],
	 2: [' #######  ', '##     ## ', '       ## ', ' #######  ', '##        ',
	       '##        ', '######### '],
	 3: [' #######  ', '##     ## ', '       ## ', ' #######  ', '       ## ',
	       '##     ## ', ' #######  '],
	 4: ['##        ', '##    ##  ', '##    ##  ', '##    ##  ', '######### ',
	       '      ##  ', '      ##  '],
	 5: [' ######## ', ' ##       ', ' ##       ', ' #######  ', '       ## ',
	       ' ##    ## ', '  ######  '],
	 6: [' #######  ', '##     ## ', '##        ', '########  ', '##     ## ',
	       '##     ## ', ' #######  '],
	 7: [' ######## ', ' ##    ## ', '     ##   ', '    ##    ', '   ##     ',
	       '   ##     ', '   ##     '],
	 8: [' #######  ', '##     ## ', '##     ## ', ' #######  ', '##     ## ',
	       '##     ## ', ' #######  '],
	 9: [' #######  ', '##     ## ', '##     ## ', ' ######## ', '       ## ',
	       '##     ## ', ' #######  '],
	 ':': ['   ', '   ', ' # ', '   ', ' # ', '   ', '   '],
        }
GLYPH_LEN = len(CLOCK[0])

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
    if hours < 9 or hours > 6:
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
    

def _create_tasks(task_dict):
    task_list = []
    for key in task_dict:
        epic_dict = task_dict[key]
        epic = Epic(epic_dict['desc'], epic_dict['open'],
                epic_dict['selected'])
        for sprint_key in epic_dict['children']:
            sprint_dict = epic_dict['children'][sprint_key]
            sprint = Sprint_Task.from_parent(epic, sprint_dict['desc'],
                    sprint_dict['open'], sprint_dict['selected'])
            for fast_key in sprint_dict['children']:
                fast_dict = sprint_dict['children'][fast_key]
                if fast_dict['blocker']:
                    Blocker.from_parent(sprint, fast_dict['desc'],
                            fast_dict['selected'])
                else:
                    Fast_Task.from_parent(sprint, fast_dict['desc'],
                            fast_dict['selected'])
        task_list.append(epic)

    return task_list

def _get_task_list():
    task_dict = {}
    task_items = []
    task_list = []
    with open(TASK_PATH, 'r') as f:
        task_dict = yaml.safe_load(f)

    task_items = _create_tasks(task_dict)

    for epic in task_items:
        task_list.append((str(epic), _get_color(epic)))
        for sprint in epic.children:
            task_list.append((str(sprint), _get_color(sprint)))
            for fast in sprint.children:
                task_list.append((str(fast), _get_color(fast))) 
    return task_list

def print_tasks(stdscr, y, max_x):
    task_list = _get_task_list()

    for y, (task_str, task_attr) in enumerate(task_list, y):
        stdscr.addstr(y, 0, task_str + ' ' * (max_x - len(task_str)),
                task_attr)

    return y, task_list

def main(stdscr):
    setup_colors()

    max_y, max_x = stdscr.getmaxyx()

    # Give line space
    next_line = print_banner(stdscr, 0, 0) + 2

    next_line, task_list = print_tasks(stdscr, next_line, max_x)

    print_clock(stdscr, max_y, max_x)

    stdscr.getch()

if __name__ == '__main__':
    curses.wrapper(main)
