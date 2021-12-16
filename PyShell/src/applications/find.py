import os
import re
from typing import Deque

from application import Application


class Find(Application):
    """Recursively searches for files with matching names
    Outputs the list of relative paths, each followed by a newline"""

    def __init__(self):
        super().__init__()

    def exec(self, args: Deque[str], out: Deque) -> None:
        if len(args) < 2:
            raise ValueError("wrong command line argument number")
        if args[-2] != "-name":
            raise ValueError("option requires an argument -- -name")
        pattern = "." + args[-1] if args[-1][0] == "*" else args[-1]
        path = "." if len(args) == 2 else args[0]
        child_dir = os.walk(path)
        for dir in child_dir:
            for file in dir[2]:
                if re.match(pattern, file):
                    out.append(f"{dir[0]}/{file}\n")
