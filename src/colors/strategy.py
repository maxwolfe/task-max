#!/usr/bin/env python3
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

# EXTEND: Create more custom strategy classes
