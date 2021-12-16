import sys
from typing import Deque

from application import Application


class Sort(Application):
    """Sorts the contents of a file/stdin line by line
    and prints the result to stdout

    The assumption of "-r" follows that,
    when sees a "-r", treat it as option,
    If there is a file "-r", use redirection or pipe"""

    def __init__(self):
        super().__init__()
        self.__option = "-r"

    def exec(self, args: Deque[str], out: Deque) -> None:
        if len(args) > 2:
            raise ValueError("wrong command line argument number")
        if len(args) == 0:
            if sys.stdin == sys.__stdin__:
                raise ValueError("no argument is given")
            lines = sys.stdin.readlines()
        if len(args) == 2 and args[0] != self.__option:
            raise ValueError(f"option requires an argument -- {self.__option}")

        if len(args) == 1 and args[0] == self.__option:  # use stdin
            if sys.stdin == sys.__stdin__:
                raise ValueError("missing file argument")
            lines = sys.stdin.readlines()

        if args and args[-1] != self.__option:
            file = args[-1]
            with open(file) as f:
                lines = f.readlines()

        lines = [line.strip() for line in lines]
        lines.sort()
        if args and args[0] == self.__option:
            lines.sort(reverse=True)
        for line in lines:
            out.append(line + "\n")
