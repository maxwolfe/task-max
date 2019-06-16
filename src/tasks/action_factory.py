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
            'j': action.MoveDown,
            'k': action.MoveUp,
            'n': action.MoveAfter,
            'N': action.MoveBefore,
            'm': action.Modify,
            'o': action.Open,
            'q': action.Quit,
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
                ActionFactory._mappings.get(key)(
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

        if action:
            action.action.do_action()
