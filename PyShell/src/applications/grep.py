import sys
import re
from typing import Deque

from application import Application


class Grep(Application):
    """Searches for lines containing a match to the specified pattern
    The output of the command is the list of lines
    Each line is printed followed by a newline"""

    def __init__(self):
        super().__init__()

    def exec(self, args: Deque[str], out: Deque) -> None:
        if len(args) == 0:
            raise ValueError("no argument is given")
        elif len(args) == 1:
            if sys.stdin == sys.__stdin__:
                raise ValueError("require an argument -- pattern or file")
        pattern = "." if args[0] == "*" else ".*%s.*" % (args[0])
        files = self.glob(list(args)[1:])
        if files:
            for file in files:
                with open(file, "r") as f:
                    lines = f.readlines()
                    for line in lines:
                        if re.match(pattern, line):
                            if len(files) > 1:
                                out.append(f"{file}:{line.strip()}\n")
                            else:
                                out.append(line.strip() + "\n")
        else:
            lines = sys.stdin.readlines()
            for line in lines:
                if re.match(pattern, line):
                    out.append(line.strip() + "\n")
