#!/usr/bin/env python3
import yaml

from uuid import uuid4

from tasks.tasks import Root
from tasks.task_factory import SubtaskFactory


class TaskList:
    def __init__(self):
        self.root = Root()

    @staticmethod
    def create_tasks(
            root,
            sub_dict,
    ):
        if not sub_dict:
            return

        for key in sub_dict:
            obj = sub_dict[key]
            new_root = SubtaskFactory.add_task(
                    root,
                    obj.get('desc'),
                    obj.get('open'),
                    obj.get('selected'),
                    obj.get('blocked'),
            )

            TaskList.create_tasks(
                    new_root,
                    obj.get('children'),
            )

    @staticmethod
    def create_dict(
            root,
            sub_dict,
    ):
        for obj in sorted(
                root.children,
                key=lambda x: x.desc,
        ):
            key = str(uuid4())
            sub_dict[key] = {
                    'desc': obj.desc,
                    'open': obj.opened,
                    'selected': obj.selected,
                    'blocked': obj.blocked,
                    'children': {},
            }

            TaskList.create_dict(
                    obj,
                    sub_dict[key]['children'],
            )

    @classmethod
    def from_yaml(
            cls,
            yaml_file,
    ):
        self = cls()
        with open(yaml_file, 'r') as f:
            task_dict = yaml.safe_load(f)

        TaskList.create_tasks(
                self.root,
                task_dict,
        )

        return self

    def to_yaml(
            self,
            yaml_file,
    ):
        task_dict = {}

        TaskList.create_dict(
                self.root,
                task_dict,
        )

        with open(yaml_file, 'w') as f:
            yaml.dump(task_dict, f)

    def get_selected(
            self,
    ):
        for task in self:
            if task.selected:
                return task

        return self.root

    def __iter__(self):
        self.current = self.root

        return self

    def __next__(self):
        nxt = self.current.find_next()

        if nxt == self.current:
            raise StopIteration('No more tasks')

        self.current = nxt

        return nxt

    def __getitem__(self, index):
        for idx, task in enumerate(self, 0):
            if index == idx:
                return task
