#!/usr/bin/env python3
import tasks.actions as action


class ActionFactory:
    # EXTEND: Key -> Action mappings
    _mappings = {
            'a': action.Add,
            'b': action.Blocker,
            'd': action.Delete,
            'e': action.Ecreate,
            'g': action.MoveTop,
            'G': action.MoveBottom,
            'h': action.Highlight,
            'H': action.Unhighlight,
            'j': action.MoveDown,
            'k': action.MoveUp,
            'n': action.MoveAfter,
            'N': action.MoveBefore,
            'm': action.Modify,
            'o': action.Open,
            'q': action.Quit,
            's': action.Save,
    }

    def __init__(
            self,
            action,
    ):
        self.action = action

    @classmethod
    def _create_action(
            cls,
            key,
            task,
            *params
    ):
        return cls(
                ActionFactory._mappings.get(
                    key,
                    ActionFactory._do_nothing,
                )(
                    task,
                    *params
                 ),
        )

    @staticmethod
    def do_action(
            key,
            task,
            *params
    ):
        action = ActionFactory._create_action(
                key,
                task,
                *params
        )

        if action.action:
            action.action.do_action()

    @staticmethod
    def _do_nothing(
            *args,
            **kwargs
    ):
        return None
