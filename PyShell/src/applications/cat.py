import sys
from typing import Deque

from application import Application


class Cat(Application):
    """Concatenates the content of given filesand prints it to stdout"""

    def __init__(self):
        super().__init__()

    def exec(self, args: Deque[str], out: Deque) -> None:
        if args:
            for a in args:
                with open(a) as f:
                    out.extend(f.readlines())
        elif sys.stdin == sys.__stdin__:
            raise ValueError("no argument is given")
        else:
            out.extend(sys.stdin.readlines())
