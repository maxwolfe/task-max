#!/usr/bin/env python3


class InvalidTask(Exception):
    pass


class Task:
    # MODIFY: Defaults
    _color = ''
    _priority = 0

    # EXTEND: Add or modify required arguments
    _required_args = [
            (
                '_desc',
                str,
            ),
            (
                '_opened',
                bool,
            ),
            (
                '_selected',
                bool,
            ),
    ]
    # EXTEND: Add or modify supported arguments
    _supported_args = [
            (
                '_blocked',
                bool,
            ),
    ]

    def __init__(
            self,
            **args
    ):
        self.parent = None
        self.children = []

        for req, typ in self._required_args:
            if req not in args.keys():
                raise InvalidTask('Missing Required Arguments')

        for key in args.keys():
            if (
                    (key, type(args[key])) in self._required_args or
                    key in self._supported_args
            ):
                setattr(
                        self,
                        key,
                        args[key],
                )

    # EXTEND: Required Args
    @property
    def desc(self):
        return self._desc

    @desc.setter
    def desc(self, desc):
        if isinstance(
                desc,
                str,
        ):
            self._desc = desc

    @property
    def opened(self):
        return self._opened

    @opened.setter
    def opened(self, opened):
        if isinstance(
                opened,
                bool,
        ):
            self._opened = opened

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, selected):
        if isinstance(
                selected,
                bool,
        ):
            self._selected = selected

    # EXTEND: Supported Args
    @property
    def blocked(self):
        for child in self.children:
            if child.blocked:
                return True

        return False


    # EXTEND: <END OF EXTEND>
    @classmethod
    def from_parent(
            cls,
            parent,
            **args
    ):
        self = cls(
                **args
        )
        parent.add_subtask(self)

        if self.selected:
            parent.open = True

        return self

    @property
    def tab_space(self):
        return '  ' * self._priority


    @property
    def color(self):
        if self.selected:
            return 'Select_{}'.format(self._color)
        else:
            return self._color

    @property
    def dict(self):
        counter = 0
        task_dict = dict()

        for arg in (self._required_args + self._supported_args):
            task_dict[arg] = getattr(
                    self,
                    arg,
            )

        if self.children:
            task_dict['children'] = {}

            for child in self.children:
                task_dict['children'][counter] = child.dict
                counter += 1

        return task_dict

    def toggle_open(
            self,
    ):
        self.open = not self.open

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
        if not self.opened or not self.children:
            return self

        return self.children[-1].get_last()

    def find_next(
            self,
    ):
        if self.opened and self.children:
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

    # TODO: Make Selection and Find Logic Extensible
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
            if self.opened:
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
                _desc='The Root',
                _selected=False,
                _opened=True,
        )

    def __str__(self):
        return ""


class Epic(Task):
    _priority = 0
    _color = 'Epic'

    def __init__(
            self,
            **args
    ):
        super().__init__(
                **args
        )


class SprintTask(Task):
    _priority = 1
    _color = 'Sprint'

    def __init__(
            self,
            **args
    ):
        super().__init__(
                **args
        )

        
class FastTask(Task):
    _priority = 2
    _color = 'Fast'

    def __init__(
            self,
            **args
    ):
        super().__init__(
                **args
        )


class Blocker(Task):
    _priority = 2
    _color = 'Blocked'

    def __init__(
            self,
            **args
    ):
        super().__init__(
                **args
        )

    @property
    def blocked(self):
        return True


class FastFactory:
    @staticmethod
    def create_task(
            parent,
            **args
    ):
        if args.get('_blocked'):
            return Blocker.from_parent(
                    parent,
                    **args
            )
        else:
            return FastTask.from_parent(
                    parent,
                    **args
            )

    @staticmethod
    def from_parent(
            parent,
            **args
    ):
        return FastFactory.create_task(
                parent,
                **args
        )
