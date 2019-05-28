#!/usr/bin/env pxthon3
import curses
import datetime
import uuid
import yaml

from collections import defaultdict
from tasks import Task_List
from time import sleep
from threading import Thread

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
GLYPH_WID = len(CLOCK[0][0])

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

def find_parent(task_dict, current):
    for epic_key in task_dict:
        epic = task_dict[epic_key]
        if epic['desc'] == current.desc:
            return task_dict
        for sprint_key in epic['children']:
            sprint = epic['children'][sprint_key]
            if sprint['desc'] == current.desc:
                return epic
            for fast_key in sprint['children']:
                fast = sprint['children'][fast_key]
                if fast['desc'] == current.desc:
                    return sprint

def find_nxt(task_dict, current):
    last = False
    for epic_key in task_dict:
        epic = task_dict[epic_key]
        if last:
            return epic
        if epic['desc'] == current.desc:
            last = True
        for sprint_key in epic['children']:
            sprint = epic['children'][sprint_key]
            if sprint['desc'] == current.desc:
                last = True
            for fast_key in sprint['children']:
                fast = sprint['children'][fast_key]
                if fast['desc'] == current.desc:
                    last = True
    return epic

def find_last(task_dict, current):
    last = None
    for epic_key in task_dict:
        epic = task_dict[epic_key]
        if not last:
            last = epic
        if epic['desc'] == current.desc:
            return last
        for sprint_key in epic['children']:
            sprint = epic['children'][sprint_key]
            if sprint['desc'] == current.desc:
                return last
            for fast_key in sprint['children']:
                fast = sprint['children'][fast_key]
                if fast['desc'] == current.desc:
                    return last
        last = epic
    return last

def find(task_dict, current):
    for epic_key in task_dict:
        epic = task_dict[epic_key]
        if epic['desc'] == current.desc:
            return epic
        for sprint_key in epic['children']:
            sprint = epic['children'][sprint_key]
            if sprint['desc'] == current.desc:
                return sprint
            for fast_key in sprint['children']:
                fast = sprint['children'][fast_key]
                if fast['desc'] == current.desc:
                    return fast
    return None

def handle_action(stdscr, action, task_list, selected, y, max_x):
    current = task_list[selected]

    task_dict = {}
    with open(TASK_PATH, 'r') as f:
        task_dict = yaml.safe_load(f)

    cur = find(task_dict, current)

    if action == 'j' and selected < len(task_list) - 1:
        nxt = find(task_dict, task_list[selected + 1])
        cur['selected'] = False
        nxt['selected'] = True
        selected += 1
    elif action == 'k' and selected > 0:
        nxt = find(task_dict, task_list[selected - 1])
        cur['selected'] = False
        nxt['selected'] = True
        selected -= 1
    elif action == 'o' and len(current.children) > 0: 
        if cur['open']:
            cur['open'] = False
        else:
            cur['open'] = True
    elif action == 'a' and (isinstance(current, Epic) or isinstance(current,
        Sprint_Task)):
        read_str = get_string(stdscr)
        read_str = read_str.decode('utf-8')
        cur['selected'] = False
        new_dict = {'desc': read_str,
                    'selected': True,
                    }
        if isinstance(current, Epic):
            new_dict['open'] = False
            new_dict['children'] = {}
        elif isinstance(current, Sprint_Task):
            new_dict['blocker'] = False

        cur['children'][str(uuid.uuid1())] = new_dict
        cur['open'] = True
    elif action == 'b' and isinstance(current, Sprint_Task):
        read_str = get_string(stdscr)
        read_str = read_str.decode('utf-8')
        cur['selected'] = False
        new_dict = {'desc': read_str,
                    'selected': True,
                    'blocker': True,
                    }
        cur['children'][str(uuid.uuid1())] = new_dict
    elif action == 'd':
        parent = find_parent(task_dict, current)
        if isinstance(current, Epic):
            children = parent
        else:
            children = parent['children']
            parent['selected'] = True

        for key in children:
            if children[key] == cur:
                del children[key]
                break
    elif action == 'g':
        cur['selected'] = False
        first = find(task_dict, task_list[0])
        first['selected'] = True
    elif action == 'G':
        cur['selected'] = False
        last = find(task_dict, task_list[-1])
        last['selected'] = True
    elif action == 'm':
        read_str = get_string(stdscr)
        read_str = read_str.decode('utf-8')
        cur['desc'] = read_str
    elif action == 'p':
        cur['selected'] = False
        parent = find_parent(task_dict, current)
        parent['selected'] = True
    elif action == 'n':
        cur['selected'] = False
        nxt = find_nxt(task_dict, current)
        nxt['selected'] = True
    elif action == 'N':
        cur['selected'] = False
        last = find_last(task_dict, current)
        last['selected'] = True
    elif action == 'e':
        read_str = get_string(stdscr)
        read_str = read_str.decode('utf-8')
        cur['selected'] = False
        new_dict = {'desc': read_str,
                    'selected': True,
                    'open': False,
                    'children': {},
                    }
        task_dict[str(uuid.uuid1())] = new_dict
        

    with open(TASK_PATH, 'w') as f:
        yaml.dump(task_dict, f)

    return selected

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
        print_tasks(stdscr, task_line, max_x)
        selected = 0
        for i, task in enumerate(task_list):
            if task.selected:
                selected = i
        task_list[selected].selected = True

        read_char = stdscr.getch()
        try:
            selected = handle_action(stdscr, chr(read_char), task_list, selected, task_line, max_x)
            next_line, task_list = print_tasks(stdscr, task_line, max_x)
            clear(stdscr, next_line, max_y - len(CLOCK[0]), max_x)
        except Exception:
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
