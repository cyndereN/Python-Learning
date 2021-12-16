import sys
from typing import Deque

from application import Application


class Uniq(Application):
    """Detects and deletes adjacent duplicate lines from
    an input file/stdin and prints the result to stdout

    The assumption of "-i" follows that,
    when sees a "-i", treat it as option,
    If there is a file "-i", use redirection or pipe"""

    def __init__(self):
        super().__init__()
        self.__option = "-i"

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
        unique = [lines[0]]
        for i in range(1, len(lines)):
            if lines[i] != lines[i - 1]:
                unique.append(lines[i])
        if args and args[0] == self.__option:
            unique_i = [unique[0]]
            for i in range(1, len(unique)):
                if unique[i].lower() != unique[i - 1].lower():
                    unique_i.append(unique[i])
            unique = unique_i
        for line in unique:
            out.append(line + "\n")
