from typing import Any, Callable


class Rule:
    def __init__(self, rule: bool, action: Callable) -> None:
        self.rule = rule
        self.action = action

    def __call__(self) -> Any:
        if self.rule:
            self.action()