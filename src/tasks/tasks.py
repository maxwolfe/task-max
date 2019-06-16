#!/usr/bin/env python3
from tasks.strategy import SelectionStrategy


class InvalidTask(Exception):
    pass


class Task:
    # MODIFY: Defaults
    _color = ''
    _priority = 0
    _selection_strategy = SelectionStrategy

    # EXTEND: Add or modify required arguments
    _required_args = [
            (
                '_desc',
                str,
            ),
            (
                '_open',
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
                raise InvalidTask('Missing Required Argument: {}\n{}'.format(
                    req,
                    args.keys(),
                    ))

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
        return self._open

    @opened.setter
    def opened(self, opened):
        if isinstance(
                opened,
                bool,
        ):
            self._open = opened

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
            parent.opened = True

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
        self.opened = not self.opened

    def toggle_select(
            self,
    ):
        self.selected = not self.selected

    # TODO: Make Selection and Find Logic Extensible
    def select(
            self,
            choice,
    ):
        mapping = {
                'next': self._selection_strategy.find_next,
                'previous': self._selection_strategy.find_previous,
                'last': self._selection_strategy.find_last,
                'first': self._selection_strategy.find_first,
                'after': self._selection_strategy.find_next_closed,
                'before': self._selection_strategy.find_previous_closed,
        }

        selected = mapping.get(choice)(self)

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
                _open=True,
        )

    def __str__(self):
        return ""


# EXTEND: Create or modify custom Task Classes
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
    _blocked = True

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


# EXTEND: Create and modify custom factories to handle custom Task creation
class Factory:
    @staticmethod
    def create_task(
            parent,
            **args
    ):
        raise NotImplementedError('Implement Custom Factory Logic')

    @classmethod
    def from_parent(
            cls,
            parent,
            **args
    ):
        return cls.create_task(
                parent,
                **args
        )


class FastFactory(Factory):
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
