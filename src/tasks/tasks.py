#!/usr/bin/env python3
import yaml

from uuid import uuid4


class InvalidTask(Exception):
    pass


class Task:
    def __init__(
            self,
            desc,
            is_open,
            is_selected
    ):
        self.desc = desc
        self.priority = 0
        self.parent = None
        self.children = []
        self._color = ''

        if is_open:
            self.is_open = True
        else:
            self.is_open = False

        if is_selected:
            self.selected = True
        else:
            self.selected = False

    @classmethod
    def from_parent(
            cls,
            parent,
            desc,
            is_open,
            is_selected
    ):
        self = cls(
                desc,
                is_open,
                is_selected,
        )
        parent.add_subtask(self)

        if is_selected:
            parent.is_open = True

        return self

    @property
    def desc(self):
        return self._desc

    @desc.setter
    def desc(self, desc):
        self._desc = desc

    @property
    def color(self):
        if self.selected:
            return 'Select_{}'.format(self._color)
        else:
            return self._color

    @property
    def is_open(self):
        return self._is_open

    @is_open.setter
    def is_open(self, opened):
        self._is_open = not (not opened)

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
        task_dict = {
                'desc': self.desc,
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

    def toggle_open(
            self,
    ):
        self.is_open = not self.is_open

    def toggle_select(
            self,
    ):
        self.selected = not self.selected

    def find_first(
            self,
    ):
        if self.parent:
            return self.parent.find_first()

        if self.children:
            return self.children[0]

        return self

    def find_last(
            self,
    ):
        return self.get_root().get_last()

    def get_root(
            self,
    ):
        if self.parent:
            return self.parent.get_root()

        return self

    def get_last(
            self,
    ):
        if not self.is_open or not self.children:
            return self

        return self.children[-1].get_last()

    def find_next(
            self,
    ):
        if self.is_open and self.children:
            return self.children[0]

        if self.parent:
            return self.parent.find_after(
                    self,
            )

        return self

    def find_after(
            self,
            task,
    ):
        task_index = self.children.index(task)

        if task_index + 1 < len(self.children):
            return self.children[task_index + 1]

        if self.parent:
            return self.parent.find_after(
                    self,
            )

        return task.get_last()

    def find_after_closed(
            self,
            task,
    ):
        task_index = self.children.index(task)

        if task_index + 1 < len(self.children):
            return self.children[task_index + 1]

        return task

    def find_next_closed(
            self,
    ):
        if self.parent:
            return self.parent.find_after_closed(
                    self,
            )

    def find_previous(
            self,
    ):
        if self.parent:
            return self.parent.find_before(
                    self,
            )

        if self.children:
            return self.children[0]

        return self

    def find_previous_closed(
            self,
    ):
        return self.parent.find_before_closed(
                self,
        )

    def find_before_closed(
            self,
            task,
    ):
        task_index = self.children.index(task)

        if task_index == 0:
            return task

        return self.children[task_index - 1]

    def find_before(
            self,
            task,
    ):
        task_index = self.children.index(task)

        if task_index == 0:
            if self.parent:
                return self

            return task

        return self.children[task_index - 1].get_last()

    def select(
            self,
            choice,
    ):
        mapping = {
                'next': self.find_next,
                'previous': self.find_previous,
                'last': self.find_last,
                'first': self.find_first,
                'after': self.find_next_closed,
                'before': self.find_previous_closed,
        }

        selected = mapping.get(choice)()

        if selected:
            self.toggle_select()
            selected.toggle_select()

    def add_subtask(
            self,
            sub_task,
    ):
        self.children.append(sub_task)
        self.children = sorted(
                self.children,
                key=lambda x: x.desc
        )
        sub_task.parent = self

    def remove_subtask(
            self,
            sub_task,
    ):
        if sub_task in self.children:
            self.children.remove(sub_task)
            self.toggle_select()

    def __del__(self):
        if self.parent:
            self.parent.remove_subtask(self)

        for child in self.children:
            del child

    def __str__(self):
        output = ''

        if len(self.children) > 0:
            if self._is_open:
                output += '{}v {}'.format(
                        self.tab_space,
                        self.desc,
                )
            else:
                output += '{}> {}'.format(
                        self.tab_space,
                        self.desc,
                )
        else:
            output += '{}  {}'.format(
                    self.tab_space,
                    self.desc,
            )

        return output

    def __eq__(self, other):
        if isinstance(
                other,
                self.__class__,
        ):
            return self.desc == other.desc

        return False


class Root(Task):
    def __init__(
            self,
    ):
        super().__init__(
                'The Root',
                True,
                False,
        )

    def __str__(self):
        return ""


class Epic(Task):
    def __init__(
            self,
            desc,
            is_open,
            is_selected,
    ):
        super().__init__(
                desc,
                is_open,
                is_selected,
        )
        self._color = 'Epic'


class Sprint_Task(Task):
    def __init__(
            self,
            desc,
            is_open,
            is_selected,
    ):
        super().__init__(
                desc,
                is_open,
                is_selected,
        )
        self.priority = 1
        self._color = 'Sprint'


class Fast_Task(Task):
    def __init__(
            self,
            desc,
            is_open,
            is_selected,
    ):
        super().__init__(
                desc,
                False,
                is_selected,
        )
        self.priority = 2
        self._color = 'Fast'


class Blocker(Task):
    def __init__(
            self,
            desc,
            is_open,
            is_selected,
    ):
        super().__init__(
                desc,
                False,
                is_selected,
        )
        self.priority = 2
        self._color = 'Blocked'

    @property
    def blocked(self):
        return True


class Fast_Factory:
    @staticmethod
    def create_task(
            parent,
            desc,
            is_selected,
            is_blocked,
    ):
        if is_blocked:
            return Blocker.from_parent(
                    parent,
                    desc,
                    False,
                    is_selected,
            )
        else:
            return Fast_Task.from_parent(
                    parent,
                    desc,
                    False,
                    is_selected,
            )

    @staticmethod
    def from_parent(
            parent,
            desc,
            is_blocked,
            is_selected,
    ):
        return Fast_Factory.create_task(
                parent,
                desc,
                is_selected,
                is_blocked,
        )


class Subtask_Factory:
    _hierarchy = [
            Root,
            Epic,
            Sprint_Task,
            Fast_Factory,
    ]

    @staticmethod
    def add_task(
            parent,
            desc,
            is_open,
            is_selected,
            is_blocker,
    ):
        task = None

        for idx, task_type in enumerate(
                Subtask_Factory._hierarchy,
        ):
            if isinstance(
                    parent,
                    task_type,
            ) and idx + 1 < len(Subtask_Factory._hierarchy):
                if idx + 2 < len(Subtask_Factory._hierarchy):
                    task = Subtask_Factory._hierarchy[idx + 1].from_parent(
                            parent,
                            desc,
                            is_open,
                            is_selected,
                    )
                else:
                    task = Subtask_Factory._hierarchy[idx + 1].from_parent(
                            parent,
                            desc,
                            is_blocker,
                            is_selected,
                    )

        return task

    @staticmethod
    def create_task(
            parent,
            desc,
            is_blocker,
    ):
        task = None

        if isinstance(
                parent,
                Root,
        ):
            task = Epic.from_parent(
                    parent,
                    desc,
                    True,
                    True,
            )
        elif isinstance(
                parent,
                Epic,
        ):
            task = Sprint_Task.from_parent(
                    parent,
                    desc,
                    True,
                    True,
            )
        elif isinstance(
                parent,
                Sprint_Task,
        ):
            task = Fast_Factory.create_task(
                    parent,
                    desc,
                    True,
                    is_blocker,
            )

        if task:
            parent.toggle_select()

            return task


class Task_List:
    def __init__(self):
        self.root = Root()

    @staticmethod
    def create_tasks(
            root,
            sub_dict,
    ):
        if not sub_dict:
            return

        for key in sub_dict:
            obj = sub_dict[key]
            new_root = Subtask_Factory.add_task(
                    root,
                    obj.get('desc'),
                    obj.get('open'),
                    obj.get('selected'),
                    obj.get('blocked'),
            )

            Task_List.create_tasks(
                    new_root,
                    obj.get('children'),
            )

    @staticmethod
    def create_dict(
            root,
            sub_dict,
    ):
        for obj in sorted(
                root.children,
                key=lambda x: x.desc,
        ):
            key = str(uuid4())
            sub_dict[key] = {
                    'desc': obj.desc,
                    'open': obj.is_open,
                    'selected': obj.selected,
                    'blocked': obj.blocked,
                    'children': {},
            }

            Task_List.create_dict(
                    obj,
                    sub_dict[key]['children'],
            )

    @classmethod
    def from_yaml(
            cls,
            yaml_file,
    ):
        self = cls()
        with open(yaml_file, 'r') as f:
            task_dict = yaml.safe_load(f)

        Task_List.create_tasks(
                self.root,
                task_dict,
        )

        return self

    def to_yaml(
            self,
            yaml_file,
    ):
        task_dict = {}

        Task_List.create_dict(
                self.root,
                task_dict,
        )

        with open(yaml_file, 'w') as f:
            yaml.dump(task_dict, f)

    def get_selected(
            self,
    ):
        for task in self:
            if task.selected:
                return task

        return self.root

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
