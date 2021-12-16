import os
from typing import Deque

from application import Application


class Pwd(Application):
    """Outputs the current working directory followed by a newline"""

    def __init__(self):
        super().__init__()

    def exec(self, args: Deque[str], out: Deque) -> None:
        if len(args) != 0:
            raise ValueError("wrong number of command line arguments")
        out.append(str(os.getcwd()) + "\n")
