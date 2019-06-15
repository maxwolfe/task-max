#!/usr/bin/env python3
from tasks.tasks import Subtask_Factory


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
                *self.params,
        )

    @classmethod
    def from_task(
            cls,
            task,
            *params
    ):
        return cls(
                task,
                *params,
        )


class Move_Down(Action):
    def __init__(
            self,
            task,
    ):
        super().__init__(
                task.select,
                'next',
        )


class Move_Up(Action):
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
                Subtask_Factory.create_task,
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
                Subtask_Factory.create_task,
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
                Subtask_Factory.create_task,
                root,
                desc,
                True,
        )
        task.toggle_select()


class Move_Top(Action):
    def __init__(
            self,
            task,
    ):
        super().__init__(
                task.select,
                'first',
        )


class Move_Bottom(Action):
    def __init__(
            self,
            task,
    ):
        super().__init__(
                task.select,
                'last',
        )


class Move_After(Action):
    def __init__(
            self,
            task,
    ):
        super().__init__(
                task.select,
                'after',
        )


class Move_Before(Action):
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


class Action_Factory:
    _mappings = {
            'a': Add,
            'b': Blocker,
            'd': Delete,
            'e': Ecreate,
            'g': Move_Top,
            'G': Move_Bottom,
            'j': Move_Down,
            'k': Move_Up,
            'n': Move_After,
            'N': Move_Before,
            'm': Modify,
            'o': Open,
            'q': Quit,
    }

    def __init__(
            self,
            action,
    ):
        self.action = action

    @classmethod
    def create_action(
            cls,
            key,
            task,
            *params
    ):
        return cls(
                Action_Factory._mappings.get(key)(
                    task,
                    *params,
                 ),
        )

    @staticmethod
    def do_action(
            key,
            task,
            *params
    ):
        action = Action_Factory.create_action(
                key,
                task,
                *params,
        )

        if action:
            action.action.do_action()
