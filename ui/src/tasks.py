#!/usr/bin/env python3


class Task:

    TAB_SPACE = '\x90' * 2

    def __init__(self, info, is_open):
        self.info = info
        self.parent = None
        self.ancestors = 0
        self.children = []
        if is_open:
            self._is_open = True
        else:
            self._is_open = False

    @classmethod
    def from_task(cls, task, info, is_open):
        self = cls(info, is_open)
        self.parent = task
        self.ancestors = self.parent.ancestors + 1
        task.add_child(self)
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

    def add_child(self, task):
        self.children.append(task)

    def remove_child(self, task):
        if task in self.children:
            self.children.remove(task)

    def __del__(self):
        if self.parent:
            self.parent.remove_child(self)
        for child in self.children:
            del child

    def __str__(self):
        output = ''
        if len(self.children) > 0:
            if self._is_open:
                output += 'v {}\n'.format(self.info)
                for child in self.children:
                    output += '{}{}'.format(self.TAB_SPACE * 
                            (self.ancestors + 1), str(child))
            else:
                output += '> {}'.format(self.info)
        else:
            output += '  {}'.format(self.info)
        return output
            

