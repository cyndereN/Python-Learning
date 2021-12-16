import os
from typing import Deque

from application import Application


class Cls(Application):
    """Clear screen method"""

    def __init__(self):
        super().__init__()

    def exec(self, args: Deque[str], out: Deque) -> None:
        if len(args) != 0:
            raise ValueError("wrong number of command line arguments")
        out.append("")
        os.system("cls" if os.name == "nt" else "clear")
