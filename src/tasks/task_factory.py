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
            **args
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
                            **args
                    )
                else:
                    task = SubtaskFactory._hierarchy[idx + 1].from_parent(
                            parent,
                            **args
                    )

        return task

    @staticmethod
    def create_task(
            parent,
            **args
    ):
        parent.toggle_select()

        return SubtaskFactory.add_task(
                parent,
                **args
        )
