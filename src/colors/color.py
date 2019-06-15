#!/usr/bin/env python3
import curses

import colors.strategy as strategy


# TODO: Make static between imports
class Colors:
    _color_pair = {
            'Highlight': curses.A_STANDOUT,
            'Blink': curses.A_BLINK,
            'Bold': curses.A_BOLD,
            'Dim': curses.A_DIM,
            'Line': curses.A_UNDERLINE,
    }
    _loader = None
    _max_colors = 512

    # MODIFY: Color defaults
    _default = 'Bold'
    _bg_default = -1
    _select_default = 238

    # EXTEND: List of strategy, filename pairs
    _strategy_list = [
            (
                strategy.CustomColorStrategy,
                'custom.yaml',
            ),
            (
                strategy.XtermColorStrategy,
                'xterm.json',
            ),
    ]

    @staticmethod
    def _load_number():
        for num in range(
                1,
                Colors._max_colors,
        ):
            yield num
        raise StopIteration

    @staticmethod
    def _load_color(int_key, str_key, byte_key, bg):
        try:
            curses.init_pair(int_key, byte_key, bg)
            Colors._color_pair[str_key] = curses.color_pair(int_key)
        except Exception:
            pass

    @staticmethod
    def _load_colors_from_dict(
            color_dict,
    ):
        for key in sorted(
                color_dict.keys(),
        ):
            color_entry = color_dict[key]
            str_key = color_entry.get('name')
            byte_key = color_entry.get('colorId')
            bg = color_entry.get(
                    'bg',
                    Colors._bg_default,
            )
            select = color_entry.get(
                    'select',
                    Colors._select_default,
            )

            try:
                if str_key and byte_key:
                    Colors._load_color(
                            next(Colors._loader),
                            str_key,
                            byte_key,
                            bg,
                    )

                    if bg != select:
                        Colors._load_color(
                                next(Colors._loader),
                                'Select_{}'.format(str_key),
                                byte_key,
                                select,
                        )
            except StopIteration:
                # Maximum Number of Colors Loaded
                return

    @staticmethod
    def _load_by_strategy(
            strategy,
    ):
        color_dict = strategy.load()
        Colors._load_colors_from_dict(
                color_dict,
        )

    @staticmethod
    def _load_colors():
        if not Colors._loader:
            curses.start_color()
            curses.use_default_colors()
            Colors._loader = Colors._load_number()

            for Strategy, filename in Colors._strategy_list:
                Colors._load_by_strategy(
                        Strategy(
                            filename,
                        ),
                )

    @staticmethod
    def get_color(
            color,
    ):
        Colors._load_colors()
        return Colors._color_pair.get(
                color,
                Colors._color_pair[Colors._default],
        )
