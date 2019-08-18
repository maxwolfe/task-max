#!/usr/bin/env python3
from tasks.task_factory import SubtaskFactory


class CleanExit(Exception):
    @staticmethod
    def call():
        raise CleanExit('Exiting Cleanly')


class SaveState(Exception):
    @staticmethod
    def call():
        raise SaveState('Save Progress')


class Action:
    def __init__(
            self,
            task_function,
            *params,
            **kwargs
    ):
        self.task_function = task_function
        self.params = params
        self.kwargs = kwargs

    def do_action(
            self,
    ):
        return self.task_function(
                *self.params,
                **self.kwargs
        )

    @classmethod
    def from_task(
            cls,
            task,
            *params,
            **kwargs
    ):
        return cls(
                task,
                *params,
                **kwargs
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
                **{
                    '_desc': desc,
                    '_open': False,
                    '_selected': True,
                }
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
                **{
                    '_desc': desc,
                    '_open': False,
                    '_selected': True,
                    '_blocked': True,
                }
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
                **{
                    '_desc': desc,
                    '_open': False,
                    '_selected': True,
                }
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


class Save(Action):
    def __init__(
            self,
            task,
    ):
        super().__init__(
                SaveState.call,
        )


# EXTEND: Create more action classes
