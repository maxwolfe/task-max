#!/usr/bin/env python3
import shared.shared as share

from datetime import datetime
from time import sleep

from colors.color import Colors
from gadgets.clock_glyphs import clock_glyphs
from shared.utils import Screen


class GlyphError(Exception):
    pass


class Clock:
    _known_times = {}

    # MODIFY: Defaults
    _default_color = 'Clock_Bad'
    _24_hour_clock = False

    # EXTEND: Color ranges + Corresponding Colors
    _color_ranges = [
            (
                (
                    9,
                    18,
                ),
                # MODIFY: Default Color for 9-7 range
                'Clock_Good',
            ),
    ]

    @staticmethod
    def _combine_glyphs(
            orig,
            to_add,
    ):
        if len(orig) != len(to_add):
            raise GlyphError('Glyph Lengths are not equal')

        for idx, glyph in enumerate(
                to_add,
        ):
            orig[idx] += glyph

        return orig

    @staticmethod
    def _val_to_glyph(
            num,
            start_zero,
    ):
        digits = []

        if num >= 10:
            digits.append(num // 10)
            num %= 10
        elif start_zero:
            digits.append(0)

        digits.append(num)
        glyphs = [''] * Clock.get_glyph_len()

        for digit in digits:
            glyph = clock_glyphs.get(digit)
            Clock._combine_glyphs(glyphs, glyph)

        return glyphs

    @staticmethod
    def _get_time():
        time_str = str(datetime.now().time())
        hours, minutes = time_str.split(':')[:2]

        return int(hours), int(minutes)

    @staticmethod
    def _load_time():
        hours, minutes = Clock._get_time()
        glyphs = Clock._known_times.get(
                (
                    hours,
                    minutes,
                ),
        )

        if not glyphs:
            glyphs = Clock._combine_glyphs(
                    Clock._val_to_glyph(
                        hours if Clock._24_hour_clock else
                        ((hours - 1) % 12) + 1,
                        False,
                    ),
                    Clock._combine_glyphs(
                        clock_glyphs.get(':').copy(),
                        Clock._val_to_glyph(
                            minutes,
                            True,
                        ),
                    ),
            )
            Clock._known_times[
                    (
                        hours,
                        minutes,
                    )
            ] = glyphs

        return (
                glyphs,
                (
                    hours,
                    minutes,
                ),
        )

    @staticmethod
    def _determine_color(
            time,
    ):
        hours, minutes = time

        for (start, end), color in Clock._color_ranges:
            if hours >= start and hours <= end:
                return Colors.get_color(color)

        return Colors.get_color(Clock._default_color)

    @staticmethod
    def _print_clock(
            stdscr,
            y,
            x,
    ):
        time_glyphs, time = Clock._load_time()
        clock_color = Clock._determine_color(time)
        center_x = x // 2 - (len(time_glyphs[0]) - 1) // 2

        for minus, line in enumerate(
                reversed(time_glyphs),
                1,
        ):
            stdscr.addstr(
                    y - minus,
                    center_x,
                    line,
                    clock_color,
            )

        return y

    @staticmethod
    def update_clock(
            stdscr,
    ):
        while True:
            with share.quit_lock:
                if share.is_quit:
                    return

            max_y, max_x = stdscr.getmaxyx()
            Screen.clean(
                    stdscr,
                    0,
                    max_x,
                    max_y - Clock.get_glyph_len(),
                    max_y,
            )
            Clock._print_clock(
                    stdscr,
                    max_y,
                    max_x,
            )
            sleep(1)

    @staticmethod
    def get_glyph_len():
        return len(clock_glyphs.get(0))
