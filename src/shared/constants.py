#!/usr/bin/env python3

from collections import defaultdict
from os import path


class GlyphError(Exception):
    pass


class CleanExit(Exception):
    pass


BASE_PATH = path.dirname(__file__)
SRC_PATH = path.join(BASE_PATH, '..')

COLOR_PATH = path.join(SRC_PATH, 'colors')
XTERM_PATH = path.join(COLOR_PATH, 'files', 'xterm.json')
CUSTOM_COLOR_PATH = path.join(COLOR_PATH, 'files', 'custom.yaml')

FILE_PATH = path.join(SRC_PATH, '..', 'files')
BANNER_PATH = path.join(FILE_PATH, 'banner')
TASK_PATH = path.join(FILE_PATH, 'tasks.yaml')


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

STRING_ACTIONS = ['a',
                  'b',
                  'e',
                  'm',
                 ]
