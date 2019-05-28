#!/usr/bin/env python3
import yaml

from uuid import uuid1


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

    @property
    def dict(self):
        counter = 0
        task_dict = {'desc': self.desc,
                     'selected': self.selected,
                    }
        if self.children:
            task_dict['open'] = self._is_open
            task_dict['children'] = {}
            for child in self.children:
                task_dict['children'][counter] = child.dict
                counter += 1
        else:
            task_dict['blocker'] = self.blocked
        return task_dict

    def toggle_select(self):
        if self.selected:
            self.selected = False
        else:
            self.selected = True

    def get_last(self):
        if not self.is_open or not self.children:
            return self

        return self.children[-1].get_last()

    def find_next(self):
        # if open and a child exists, select first one
        if self.is_open and self.children:
            return self.children[0]
        
        # if a parent exists, ask it to find next lower than you
        if self.parent:
            return self.parent.find_after(self)

    # find after if possible
    def find_after(self, task):
        task_index = self.children.index(task)

        if task_index + 1 < len(self.children):
            return self.children[task_index + 1]

        return self.parent.find_after(self)

    def find_previous(self):
        return self.parent.find_before(self)

    def find_before(self, task):
        task_index = self.children.index(task)

        if task_index == 0:
            return self
        return self.children[task_index - 1]

    def select_next(self):
        nxt = self.find_next()

        self.toggle_select()
        nxt.toggle_select()

    def select_previous(self):
        prev = self.find_previous()

        self.toggle_select()
        prev.toggle_select()

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
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.desc == other.desc
        return False
            

class Root(Task):
    def __init__(self):
        super().__init__('The Root', False, False)

    def find_next(self):
        if self.children:
            return self.children[0]
        return self

    def find_pevious(self):
        return self

    def find_after(self, task):
        task_index = self.children.index(task)

        if task_index + 1 < len(self.children):
            return self.children[task_index + 1]

        return task.get_last()

    def find_before(self, task):
        task_index = self.children.index(task)

        if task_index == 0:
            return task
        return self.children[task_index - 1]

    def __str__(self):
        return None


class Epic(Task):
    def __init__(self, desc, is_open, is_selected):
        super().__init__(desc, is_open, is_selected)

    @classmethod
    def from_parent(cls, parent, desc, is_open, is_selected):
        if not isinstance(parent, Root):
            raise InvalidTask("Sprint Task must be created from an Epic")
        return super().from_parent(parent, desc, is_open, is_selected)


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


class Fast_Factory:
    @staticmethod
    def create_task(parent, desc, is_selected, is_blocked):
        if is_blocked:
            return Blocker.from_parent(parent, desc, is_selected)
        else:
            return Fast_Task.from_parent(parent, desc, is_selected)


class Task_List:
    def __init__(self):
        self.root = Root()

    @classmethod
    def from_yaml(cls, yaml_file):
        self = cls()
        with open(yaml_file, 'r') as f:
            task_dict = yaml.safe_load(f)

        for epic_key in task_dict:
            epic = task_dict[epic_key]
            Epic.from_parent(self.root,
                             epic['desc'],
                             epic['open'],
                             epic['selected'],
                             )
            for sprint_key in epic['children']:
                sprint = epic['children'][sprint_key]
                Sprint_Task.from_parent(epic,
                                        sprint['desc'],
                                        sprint['open'],
                                        sprint['selected'],
                                        )
                for fast_key in sprint['children']:
                    fast = epic['children'][fast_key]
                    is_blocked = fast.get('blocker')
                    Fast_Factory.create_task(sprint,
                                             fast['desc'],
                                             fast['open'],
                                             fast['selected'],
                                             is_blocked,
                                             )
        return self

    def to_yaml(self, yaml_file):
        task_dict = {}

        for epic in root.children:
            epic_key = uuid1()
            task_dict[epic_key] = {'desc': epic.desc,
                                   'open':  epic.is_open,
                                   'selected': epic.selected,
                                   'children': {},
                                  }
            epic_dict = task_dict[epic_key]['children']
            for sprint in epic.children:
                sprint_key = uuid1()
                epic_dict[sprint_key] = {'desc': sprint.desc,
                                         'open':  sprint.is_open,
                                         'selected': sprint.selected,
                                         'children': {},
                                      }
                sprint_dict = epic_dict[sprint_key]['children']
                for fast in sprint.children:
                    fast_key = uuid1()
                    sprint_dict[fast_key] = {'desc': fast.desc,
                                             'open':  fast.is_open,
                                             'selected': fast.selected,
                                             'blocked': fast.blocked
                                            }

        with open(yaml_file, 'w') as f:
            f.write(task_dict)

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
