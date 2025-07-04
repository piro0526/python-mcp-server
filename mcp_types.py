from typing import Any, Callable, Dict


class Tool:
    def __init__(
        self,
        definition: Dict[str, Any],
        callback: Callable,
    ):
        self.definition = definition
        self.callback = callback
