#!/usr/bin/env python3
from colors.color import Colors
from shared.utils import Screen


class LineNumbers:
    _num_length = 4

    @staticmethod
    def _get_color(
            difference,
    ):
        if difference < 0:
            return Colors.get_color(
                    'LineNeg',
            )
        elif difference > 0:
            return Colors.get_color(
                    'LinePos',
            )
        else:
            return Colors.get_color(
                    'LineNeut',
            )

    @staticmethod
    def update_line_nums(
            stdscr,
            start,
            end,
            cur,
    ):
        """
        Update line numbers relative to current item
        """

        Screen.clean(
                stdscr,
                0,
                LineNumbers._num_length,
                start,
                end,
        )

        for line in range(
                start,
                end,
        ):
            stdscr.addstr(
                    line,
                    0,
                    str(
                        abs(
                            line - start - cur,
                        ),
                    ),
                    LineNumbers._get_color(
                        line - start - cur,
                    ),
            )
