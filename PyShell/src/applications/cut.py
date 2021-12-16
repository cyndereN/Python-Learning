import sys
from typing import Deque, TextIO

from application import Application


class Cut(Application):
    """class that implement the cut application

    The assumption of the -b options follows that,
    "-b will only work on input lines of less than 1023 bytes"
    quote from this link: https://en.wikipedia.org/wiki/Cut_(Unix)#Syntax
    Where the link is given in application.md
    """

    def __init__(self):
        super().__init__()
        self.__options = {"-b": self.__byte_extract_option}
        self.__bytes_to_read = None

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
                    self.__exec(opened_file, out)
        else:
            self.__exec(sys.stdin, out)

    def __exec(self, file: TextIO, out: Deque):
        if not self.__bytes_to_read:
            raise ValueError("usage: cut -b list [file ...]")
        else:
            for line in file.readlines():
                line = line.encode()
                line_length = len(line)
                result = ""
                for byte in self.__bytes_to_read:
                    if byte >= line_length:
                        break
                    result += bytes([line[byte]]).decode()
                result = ("").join(result).replace("\n", "")
                out.append(result + "\n")

    def __byte_extract_option(self, args: Deque[str]):
        bytes_to_read = set()
        if len(args) == 0:
            raise ValueError("option requires an argument -- b")
        option_args = args.popleft().split(",")
        option_args = [byte.split("-") for byte in option_args]
        for outer, option_arg in enumerate(option_args):
            for inner, byte_index in enumerate(option_arg):
                if byte_index.isnumeric():
                    option_args[outer][inner] = int(byte_index)
                elif byte_index == "":
                    continue
                else:
                    raise ValueError("illegal list count")
        for option_arg in option_args:
            if len(option_arg) == 0:
                raise ValueError("values may not include zero")
            elif len(option_arg) == 1:  # case one byte exactly
                bytes_to_read.add(
                    option_arg[0] - 1
                )  # index in shell begin at 0
            elif len(option_arg) == 2:  # case byte in interval
                if option_arg[0] == "":
                    option_arg[0] = 0
                if option_arg[1] == "":
                    option_arg[1] = 1023
                if option_arg[1] < option_arg[0]:
                    continue
                for byte in range(option_arg[0], option_arg[1] + 1):
                    bytes_to_read.add(byte - 1)  # index in shell begin at 0
            else:
                raise ValueError("illegal list count")
        bytes_to_read = list(bytes_to_read)
        bytes_to_read.sort()
        self.__bytes_to_read = bytes_to_read
