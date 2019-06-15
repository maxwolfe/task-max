#!/usr/bin/env python3
from os import path


class FileSearcher:
    @staticmethod
    def find_file(
            request_file,
            filename,
    ):
        base_path = path.dirname(request_file)
        files_path = path.join(
                base_path,
                'files'
        )

        return path.join(
                files_path,
                filename
        )


class Screen:
    @staticmethod
    def clean(
            stdscr,
            x_start,
            x_end,
            y_start,
            y_end,
    ):
        for y in range(
                y_start,
                y_end,
        ):
            stdscr.addstr(
                    y,
                    x_start,
                    ' ' * (x_end - x_start - 1),
            )

    @staticmethod
    def clear(
            stdscr,
            top,
            bottom,
            max_x,
    ):
        return Screen.clean(
                stdscr,
                0,
                max_x + 1,
                top + 1,
                bottom,
        )
