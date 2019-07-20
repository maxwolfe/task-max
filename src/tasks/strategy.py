#!/usr/bin/env python3


class SelectionStrategy:
    @staticmethod
    def find_first(
            req_task,
    ):
        if req_task.parent:
            return SelectionStrategy.find_first(
                    req_task.parent,
            )

        if req_task.children:
            return req_task.children[0]

        return req_task

    @staticmethod
    def find_last(
            req_task,
    ):
        return SelectionStrategy.get_last(
                SelectionStrategy.get_root(
                    req_task,
                ),
        )

    @staticmethod
    def get_root(
            req_task,
    ):
        if req_task.parent:
            return SelectionStrategy.get_root(
                    req_task.parent,
            )

        return req_task

    @staticmethod
    def get_last(
            req_task,
    ):
        if not req_task.opened or not req_task.children:
            return req_task

        return SelectionStrategy.get_last(
                req_task.children[-1],
        )

    @staticmethod
    def find_next(
            req_task,
    ):
        if req_task.opened and req_task.children:
            return req_task.children[0]

        if req_task.parent:
            return SelectionStrategy.find_after(
                    req_task.parent,
                    req_task,
            )

        return req_task

    @staticmethod
    def find_after(
            req_task,
            task,
    ):
        task_index = req_task.children.index(task)

        if task_index + 1 < len(req_task.children):
            return req_task.children[task_index + 1]

        if req_task.parent:
            return SelectionStrategy.find_after(
                    req_task.parent,
                    req_task,
            )

        return SelectionStrategy.get_last(
                task,
        )

    @staticmethod
    def find_after_closed(
            req_task,
            task,
    ):
        task_index = req_task.children.index(task)

        if task_index + 1 < len(req_task.children):
            return req_task.children[task_index + 1]

        return task

    @staticmethod
    def find_next_closed(
            req_task,
    ):
        if req_task.parent:
            return SelectionStrategy.find_after_closed(
                    req_task.parent,
                    req_task,
            )

    @staticmethod
    def find_previous(
            req_task,
    ):
        if req_task.parent:
            return SelectionStrategy.find_before(
                    req_task.parent,
                    req_task,
            )

        if req_task.children:
            return req_task.children[0]

        return req_task

    @staticmethod
    def find_previous_closed(
            req_task,
    ):
        return SelectionStrategy.find_before_closed(
                req_task.parent,
                req_task,
        )

    @staticmethod
    def find_before_closed(
            req_task,
            task,
    ):
        task_index = req_task.children.index(task)

        if task_index == 0:
            return task

        return req_task.children[task_index - 1]

    @staticmethod
    def find_before(
            req_task,
            task,
    ):
        task_index = req_task.children.index(task)

        if task_index == 0:
            if req_task.parent:
                return req_task

            return task

        return SelectionStrategy.get_last(
                req_task.children[task_index - 1],
        )

# EXTEND: Create more Selection Strategies
