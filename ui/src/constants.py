from collections import defaultdict


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

STRING_ACTIONS = ['a',
                  'b',
                  'e',
                 ]
