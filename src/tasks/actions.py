#!/usr/bin/env python3
from tasks.task_factory import SubtaskFactory


class CleanExit(Exception):
    @staticmethod
    def call():
        raise CleanExit('Exiting Cleanly')


class Action:
    def __init__(
            self,
            task_function,
            *params
    ):
        self.task_function = task_function
        self.params = params

    def do_action(
            self,
    ):
        return self.task_function(
                *self.params
        )

    @classmethod
    def from_task(
            cls,
            task,
            *params
    ):
        return cls(
                task,
                *params
        )


class MoveDown(Action):
    def __init__(
            self,
            task,
    ):
        super().__init__(
                task.select,
                'next',
        )


class MoveUp(Action):
    def __init__(
            self,
            task
    ):
        super().__init__(
                task.select,
                'previous'
        )


class Open(Action):
    def __init__(
            self,
            task,
    ):
        super().__init__(
                task.toggle_open,
        )


class Add(Action):
    def __init__(
            self,
            task,
            desc,
    ):
        super().__init__(
                SubtaskFactory.create_task,
                task,
                desc,
                False,
        )


class Blocker(Action):
    def __init__(
            self,
            task,
            desc,
    ):
        super().__init__(
                SubtaskFactory.create_task,
                task,
                desc,
                True,
        )


class Delete(Action):
    def __init__(
            self,
            task,
    ):
        super().__init__(
                task.__del__,
        )


class Ecreate(Action):
    def __init__(
            self,
            task,
            desc,
    ):
        root = task.get_root()
        super().__init__(
                SubtaskFactory.create_task,
                root,
                desc,
                True,
        )
        task.toggle_select()


class MoveTop(Action):
    def __init__(
            self,
            task,
    ):
        super().__init__(
                task.select,
                'first',
        )


class MoveBottom(Action):
    def __init__(
            self,
            task,
    ):
        super().__init__(
                task.select,
                'last',
        )


class MoveAfter(Action):
    def __init__(
            self,
            task,
    ):
        super().__init__(
                task.select,
                'after',
        )


class MoveBefore(Action):
    def __init__(
            self,
            task,
    ):
        super().__init__(
                task.select,
                'before',
        )


class Modify(Action):
    def __init__(
            self,
            task,
            desc,
    ):
        super().__init__(
                setattr,
                task,
                'desc',
                desc,
        )


class Quit(Action):
    def __init__(
            self,
            task,
    ):
        super().__init__(
                CleanExit.call,
        )

# EXTEND: Create more action classes
