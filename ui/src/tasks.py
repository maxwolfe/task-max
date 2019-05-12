#!/usr/bin/env python3

class InvalidTask(Exception):
    pass

class Task:
    def __init__(self, desc, is_open, is_selected):
        self.desc = desc
        self.priority = 0
        self.parent = None
        self.children = []
        if is_open:
            self._is_open = True
        else:
            self._is_open = False
        if is_selected:
            self.selected= True
        else:
            self.selected = False

    @classmethod
    def from_parent(cls, parent, desc, is_open, is_selected):
        self = cls(desc, is_open, is_selected)
        parent.add_subtask(self)
        return self

    @property
    def is_open(self):
        return self._is_open

    @is_open.setter
    def is_open(self, opened):
        if opened and len(self.children) > 0:
            self._is_open = True
        else:
            self._is_open = False

    @property
    def tab_space(self):
        return '  ' * self.priority

    @property
    def blocked(self):
        for child in self.children:
            if child.blocked:
                return True
        return False

    def add_subtask(self, sub_task):
        self.children.append(sub_task)
        sub_task.parent = self

    def remove_subtask(self, sub_task):
        if sub_task in self.children:
            self.children.remove(sub_task)

    def __del__(self):
        if self.parent:
            self.parent.remove_subtask(self)
        for child in self.children:
            del child

    def __str__(self):
        output = ''
        if len(self.children) > 0:
            if self._is_open:
                output += '{}v {}'.format(self.tab_space, self.desc)
            else:
                output += '{}> {}'.format(self.tab_space, self.desc)
        else:
            output += '{}  {}'.format(self.tab_space, self.desc)

        return output
            
class Epic(Task):
    def __init__(self, desc, is_open, is_selected):
        super().__init__(desc, is_open, is_selected)

    @classmethod
    def from_parent(cls, parent, desc, is_open, is_selected):
        raise InvalidTask("Epic be created from a parent")

class Sprint_Task(Task):
    def __init__(self, desc, is_open, is_selected):
        super().__init__(desc, is_open, is_selected)
        self.priority = 1

    @classmethod
    def from_parent(cls, parent, desc, is_open, is_selected):
        if not isinstance(parent, Epic):
            raise InvalidTask("Sprint Task must be created from an Epic")
        return super().from_parent(parent, desc, is_open, is_selected)

class Fast_Task(Task):
    def __init__(self, desc, is_open, is_selected):
        super().__init__(desc, False, is_selected)
        self.priority = 2

    @classmethod
    def from_parent(cls, parent, desc, is_selected):
        if not isinstance(parent, Sprint_Task):
            raise InvalidTask("Fast Task must be created from a Sprint Task")
        return super().from_parent(parent, desc, False, is_selected)

class Blocker(Task):
    def __init__(self, desc, is_open, is_selected):
        super().__init__(desc, False, is_selected)
        self.priority = 2

    @classmethod
    def from_parent(cls, parent, desc, is_selected):
        if not isinstance(parent, Sprint_Task):
            raise InvalidTask("Blocker must be created from a Sprint Task")
        return super().from_parent(parent, desc, False, is_selected)

    @property
    def blocked(self):
        return True
