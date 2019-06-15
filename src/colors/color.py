#!/usr/bin/env python3
import curses
import json
import yaml

from shared.utils import FileSearcher


class LoadStrategy:
    def __init__(
            self,
            file_name,
    ):
        self.file_path = FileSearcher.find_file(
                __file__,
                file_name,
        )

    def _load_yaml(
            self,
    ):
        try:
            with open(self.file_path, 'r') as f:
                return yaml.safe_load(f.read())
        except FileNotFoundError:
            return dict()

    def _load_json(
            self,
    ):
        try:
            with open(self.file_path, 'r') as f:
                return json.loads(f.read())
        except FileNotFoundError:
            return list()

    def load(
            self,
    ):
        raise NotImplementedError('Must Implement Strategy')


class CustomColorStrategy(LoadStrategy):
    def load(
            self,
    ):
        return self._load_yaml()


class XtermColorStrategy(LoadStrategy):
    def load(
            self,
    ):
        color_list = self._load_json()
        color_dict = dict()

        for key, data in enumerate(
                color_list,
        ):
            color_dict[key] = data

        return color_dict


# TODO: Make static between imports
class Colors:
    _color_pair = {
            'Highlight': curses.A_STANDOUT,
            'Blink': curses.A_BLINK,
            'Bold': curses.A_BOLD,
            'Dim': curses.A_DIM,
            'Line': curses.A_UNDERLINE,
    }
    _default = 'Bold'
    _bg_default = -1
    _select_default = 238
    _loader = None
    _max_colors = 512

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
            Colors._load_by_strategy(
                    CustomColorStrategy(
                        'custom.yaml',
                    ),
            )
            Colors._load_by_strategy(
                    XtermColorStrategy(
                        'xterm.json',
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
