import os
from os import listdir
from typing import Deque

from application import Application


class Ls(Application):
    """Lists the content of a directory, it prints a list of files
    and directories separated by tabs and followed by a newline
    Ignores files and directories whose names start with ."""

    def __init__(self):
        super().__init__()

    def exec(self, args: Deque[str], out: Deque) -> None:
        if len(args) == 0:
            ls_dir = os.getcwd()
        elif len(args) > 1:
            raise ValueError("wrong number of command line arguments")
        else:
            ls_dir = args[0]
        for f in listdir(ls_dir):
            if not f.startswith("."):
                out.append(f + "\n")
