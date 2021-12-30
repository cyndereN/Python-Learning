from abc import ABCMeta, abstractmethod
from typing import List, Deque

from evaluator import Visitor


class Command(metaclass=ABCMeta):  # pragma: no cover
    """Command interface"""

    def __init__(self):
        pass

    @abstractmethod
    def accept(self, visitor: Visitor, out: Deque) -> None:
        pass


class Call(Command):
    def __init__(self):
        super().__init__()
        self.application: str = None
        self.is_unsafe: bool = None
        self.args: Deque[str] = []
        self.stdin: str = None
        self.stdout: str = None

    def accept(self, visitor: Visitor, out: Deque) -> None:
        return visitor.visit_call(self, out)


class Sequence(Command):
    def __init__(self, command: Command):
        super().__init__()
        self._command_sequence: List[Command] = [command]

    def accept(self, visitor: Visitor, out: Deque) -> None:
        return visitor.visit_sequence(self, out)

    def add_command(self, command: Command) -> None:
        self._command_sequence.append(command)

    @property
    def command_sequence(self) -> List[Command]:
        return self._command_sequence


class Pipe(Command):
    def __init__(self, call):
        super().__init__()
        self._command_pipe: List[Call] = [call]

    def accept(self, visitor: Visitor, out: Deque) -> None:
        return visitor.visit_pipe(self, out)

    def add_command(self, command: Call) -> None:
        self._command_pipe.append(command)

    @property
    def command_pipe(self) -> List[Call]:
        return self._command_pipe
