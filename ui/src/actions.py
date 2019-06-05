#!/usr/bin/env python3

from tasks import Subtask_Factory

class Action:
    def __init__(self, task_function, *params):
        self.task_function = task_function
        self.params = params

    def do_action(self):
        return self.task_function(*self.params)


class Move_Down(Action):
    def __init__(self, task):
        super().__init__(task.select, 'next')

    @classmethod
    def from_task(cls, task):
        return cls(task)


class Move_Up(Action):
    def __init__(self, task):
        super().__init__(task.select, 'previous')

    @classmethod
    def from_task(cls, task):
        return cls(task)


class Open(Action):
    def __init__(self, task):
        super().__init__(task.toggle_open)

    @classmethod
    def from_task(cls, task):
        return cls(task)


class Add(Action):
    def __init__(self, task, desc):
        super().__init__(Subtask_Factory.create_task, task, desc, False)

    @classmethod
    def from_task(cls, task, desc):
        return cls(task, desc)


class Blocker(Action):
    def __init__(self, task, desc):
        super().__init__(Subtask_Factory.create_task, task, desc, True)

    @classmethod
    def from_task(cls, task, desc):
        return cls(task, desc)


class Delete(Action):
    def __init__(self, task):
        super().__init__(task.__del__)

    @classmethod
    def from_task(cls, task):
        return cls(task)

class Ecreate(Action):
    def __init__(self, task, desc):
        root = task.get_root()
        super().__init__(Subtask_Factory.create_task, root, desc, True)
        task.toggle_select()

    @classmethod
    def from_task(cls, task, desc):
        return cls(task, desc)

class Move_Top(Action):
    def __init__(self, task):
        super().__init__(task.select, 'first')
    
    @classmethod
    def from_task(cls, task):
        return cls(task)

class Move_Bottom(Action):
    def __init__(self, task):
        super().__init__(task.select, 'last')

    @classmethod
    def from_task(cls, task):
        return cls(task)

class Move_After(Action):
    def __init__(self, task):
        super().__init__(task.select, 'after')

    @classmethod
    def from_task(cls, task):
        return cls(task)

class Move_Before(Action):
    def __init__(self, task):
        super().__init__(task.select, 'before')

    @classmethod
    def from_task(cls, task):
        return cls(task)

class Action_Factory:
    def __init__(self, action):
        self.action = action

    @classmethod
    def create_action(cls, key, task, *params):
        if key == 'a':
            return cls(Add(task, *params))
        elif key == 'b':
            return cls(Blocker(task, *params))
        elif key == 'd':
            return cls(Delete(task))
        elif key == 'e':
            return cls(Ecreate(task, *params))
        elif key == 'g':
            return cls(Move_Top(task))
        elif key == 'G':
            return cls(Move_Bottom(task))
        elif key == 'j':
            return cls(Move_Down(task))
        elif key == 'k':
            return cls(Move_Up(task))
        elif key == 'n':
            return cls(Move_After(task))
        elif key == 'N':
            return cls(Move_Before(task))
        elif key =='o':
            return cls(Open(task))
        
    @staticmethod
    def do_action(key, task, *params):
        action = Action_Factory.create_action(key, task, *params)
        if action:
            action.action.do_action()

