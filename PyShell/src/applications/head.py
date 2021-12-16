import sys
from typing import Deque, TextIO

from application import Application


class Head(Application):
    """Prints the first N lines of a given file or stdin
    If there are less than N lines, prints only the existing
    lines without raising an exception"""

    def __init__(self):
        super().__init__()
        self.__options = {"-n": self.__line_count_option}
        self.__read_line_number = 10

    def exec(self, args: Deque[str], out: Deque) -> None:
        if len(args) == 0:
            if sys.stdin == sys.__stdin__:
                raise ValueError("no argument is given")
            else:
                pass  # valid, use stdin
        while len(args) > 0 and args[0] in self.__options:
            self.__options[args.popleft()](args)
        args = self.glob(args)
        if args:
            for file in args:
                with open(file, "r") as opened_file:
                    self.__exec(opened_file, self.__read_line_number, out)
        else:
            self.__exec(sys.stdin, self.__read_line_number, out)

    def __exec(self, file: TextIO, read_line_number: int, out: Deque):
        for i in range(0, read_line_number):
            line = file.readline()
            if not line:
                break
            out.append(line)

    def __line_count_option(self, args: Deque[str]):
        if len(args) == 0:
            raise ValueError("option requires an argument -- n")
        else:
            option_arg = args.popleft()
            if not option_arg.isnumeric():
                raise ValueError(f"illegal line count -- {option_arg}")
            else:
                option_arg = int(option_arg)
                if option_arg > 0:
                    self.__read_line_number = option_arg
                else:
                    raise ValueError(f"illegal line count -- {option_arg}")
