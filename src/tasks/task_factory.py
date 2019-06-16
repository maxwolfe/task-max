#!/usr/bin/env python3
import tasks.tasks as tasks


class SubtaskFactory:
    # EXTEND: Create custom hierarchy or extend hierarchy
    _hierarchy = [
            tasks.Root,
            tasks.Epic,
            tasks.SprintTask,
            tasks.FastFactory,
    ]

    @staticmethod
    def add_task(
            parent,
            desc,
            is_open,
            is_selected,
            is_blocker,
            **extras
    ):
        task = None

        for idx, task_type in enumerate(
                SubtaskFactory._hierarchy,
        ):
            if isinstance(
                    parent,
                    task_type,
            ) and idx + 1 < len(SubtaskFactory._hierarchy):
                if idx + 2 < len(SubtaskFactory._hierarchy):
                    task = SubtaskFactory._hierarchy[idx + 1].from_parent(
                            parent,
                            _desc=desc,
                            _opened=is_open,
                            _selected=is_selected,
                    )
                else:
                    task = SubtaskFactory._hierarchy[idx + 1].from_parent(
                            parent,
                            _desc=desc,
                            _opened=is_open,
                            _selected=is_selected,
                            _blocked=is_blocker,
                    )

        return task

    @staticmethod
    def create_task(
            parent,
            desc,
            is_blocker,
            **extras
    ):
        parent.toggle_select()

        return SubtaskFactory.add_task(
                parent,
                desc,
                True,
                True,
                is_blocker,
                **extras
        )
