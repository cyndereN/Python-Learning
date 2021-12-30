import re
import os
import sys
from os import listdir
from abc import ABCMeta, abstractmethod
from glob import glob
from typing import Deque, TextIO


class Application(metaclass=ABCMeta):  # pragma: no cover
    """Application Interface"""

    def __init__(self):
        pass

    @abstractmethod
    def exec(self, args: Deque[str], out: Deque) -> None:
        pass

    def glob(self, args: Deque[str] = []):
        globbed = []
        for arg in args:
            globbing = glob(arg)
            if globbing:
                globbed.extend(globbing)
            else:
                globbed.append(arg)
        return globbed


class UnsafeApplicationProxy(Application):  # pragma: no cover
    """The proxy of Application, carry the unsafe mode

    The assumption of our unsafe mode is that
    It is unsafe in terms of an application support by our shell,
    e.g. _ls, _echo and _pwd.
    Otherwise, it will throws the exception and halts,
    e.g _sing.
    """

    def __init__(self, application: Application) -> None:
        super().__init__()
        self._application = application

    def exec(self, args: Deque[str], out: Deque) -> None:
        try:
            self._application.exec(args, out)
            self.log_access()
        except (ValueError, FileNotFoundError) as e:
            print(e)

    def log_access(self) -> None:
        print("[Proxy: Logging unsafe mode.]", end="")


class Pwd(Application):
    """Outputs the current working directory followed by a newline"""

    def __init__(self):
        super().__init__()

    def exec(self, args: Deque[str], out: Deque) -> None:
        if len(args) != 0:
            raise ValueError("wrong number of command line arguments")
        out.append(str(os.getcwd()) + "\n")


class Cd(Application):
    """Changes the current working directory"""

    def __init__(self):
        super().__init__()

    def exec(self, args: Deque[str], out: Deque) -> None:
        if len(args) != 1:
            raise ValueError("wrong number of command line arguments")
        out.append("")
        os.chdir(args[0])


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
        for file_and_dir in listdir(ls_dir):
            if not file_and_dir.startswith("."):
                out.append(file_and_dir + "\n")


class Cat(Application):
    """Concatenates the content of given filesand prints it to stdout"""

    def __init__(self):
        super().__init__()

    def exec(self, args: Deque[str], out: Deque) -> None:
        if args:
            args = self.glob(args)
            for arg in args:
                with open(arg) as file:
                    out.extend(file.readlines())
        elif sys.stdin == sys.__stdin__:
            raise ValueError("no argument is given")
        else:
            out.extend(sys.stdin.readlines())


class Echo(Application):
    """Prints its arguments separated by spaces
    and followed by a newline to stdout"""

    def __init__(self):
        super().__init__()

    def exec(self, args: Deque[str], out: Deque) -> None:
        args = self.glob(args)
        out.append(" ".join(args) + "\n")


class Head(Application):
    """Prints the first N lines of a given file or stdin
    If there are less than N lines, prints only the existing
    lines without raising an exception"""

    def __init__(self):
        super().__init__()
        self.__options = {"-n": self.__line_count_option}
        self.__read_line_number = 10

    def exec(self, args: Deque[str], out: Deque) -> None:
        while len(args) > 0 and args[0] in self.__options:
            self.__options[args.popleft()](args)
        if len(args) == 0 and sys.stdin == sys.__stdin__:
            raise ValueError("no argument is given")
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
        option_arg = args.popleft()
        if not option_arg.isnumeric():
            raise ValueError(f"illegal line count -- {option_arg}")
        option_arg = int(option_arg)
        if option_arg <= 0:
            raise ValueError(f"illegal line count -- {option_arg}")
        self.__read_line_number = option_arg


class Tail(Application):
    """Prints the last N lines of a given file or stdin
    If there are less than N lines, prints only the existing
    lines without raising an exception"""

    def __init__(self):
        super().__init__()
        self.__options = {"-n": self.__line_count_option}
        self.__read_line_number = 10

    def exec(self, args: Deque[str], out: Deque) -> None:
        while len(args) > 0 and args[0] in self.__options:
            self.__options[args.popleft()](args)
        if len(args) == 0 and sys.stdin == sys.__stdin__:
            raise ValueError("no argument is given")
        args = self.glob(args)
        if args:
            for file in args:
                with open(file, "r") as opened_file:
                    self.__exec(opened_file, self.__read_line_number, out)
        else:
            self.__exec(sys.stdin, self.__read_line_number, out)

    def __exec(self, file: TextIO, read_line_number: int, out: Deque):
        lines = file.readlines()
        total_line_number = len(lines)
        begin_line_number = max(0, total_line_number - read_line_number)
        out.extend(lines[begin_line_number:])

    def __line_count_option(self, args: Deque[str]):
        if len(args) == 0:
            raise ValueError("option requires an argument -- n")
        option_arg = args.popleft()
        if not option_arg.isnumeric():
            raise ValueError(f"illegal line count -- {option_arg}")
        option_arg = int(option_arg)
        if option_arg <= 0:
            raise ValueError(f"illegal line count -- {option_arg}")
        self.__read_line_number = option_arg


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


class Cut(Application):
    """class that implement the cut application

    The assumption of the -b options follows that,
    "-b will only work on input lines of less than 1023 bytes"
    quote from this link: https://en.wikipedia.org/wiki/Cut_(Unix)#Syntax
    Where the link is given in application.md
    Another assumption is that
    this cut application with not stop users to give an decreasing range.
    i.e. it would not raises an exception, but ignore that range.
    """

    def __init__(self):
        super().__init__()
        self.__options = {"-b": self.__byte_extract_option}
        self.__bytes_to_read = None

    def exec(self, args: Deque[str], out: Deque) -> None:
        while len(args) > 0 and args[0] in self.__options:
            self.__options[args.popleft()](args)
        if len(args) == 0 and sys.stdin == sys.__stdin__:
            raise ValueError("no argument is given")
        args = self.glob(args)
        if args:
            for file in args:
                with open(file, "r") as opened_file:
                    self.__exec(opened_file, out)
        else:
            self.__exec(sys.stdin, out)

    def __exec(self, file: TextIO, out: Deque):
        if self.__bytes_to_read is None:
            raise ValueError("usage: cut -b list [file ...]")
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
        self.__bytes_to_read = []
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
            if option_arg.count("") == 2:  # both side of the interval is empty
                raise ValueError("values may not include zero")
            if len(option_arg) == 1:  # case one byte exactly
                bytes_to_read.add(
                    option_arg[0] - 1
                )  # index in shell begin at 0
            elif len(option_arg) == 2:  # case byte in interval
                if option_arg[0] == "":
                    option_arg[0] = 1
                if option_arg[1] == "":
                    option_arg[1] = 1023
                if option_arg[1] < option_arg[0]:
                    continue
                for byte in range(option_arg[0], option_arg[1] + 1):
                    bytes_to_read.add(byte - 1)  # index in shell begin at 0
            else:
                raise ValueError("illegal list count")
        if -1 in bytes_to_read:  # case 0 is in the args
            raise ValueError("values may not include zero")
        bytes_to_read = list(bytes_to_read)
        bytes_to_read.sort()
        self.__bytes_to_read = bytes_to_read


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


class Uniq(Application):
    """Detects and deletes adjacent duplicate lines from
    an input file/stdin and prints the result to stdout

    The assumption of "-i" follows that,
    when sees a "-i", treat it as option,
    If there is a file "-i", use redirection or pipe"""

    def __init__(self):
        super().__init__()
        self.__options = {"-i": self.__ignore_case_option}
        self.__is_case_insensitive = False

    def exec(self, args: Deque[str], out: Deque) -> None:
        while len(args) > 0 and args[0] in self.__options:
            self.__options[args.popleft()]()
        lines = []
        if len(args) == 0:
            if sys.stdin == sys.__stdin__:
                raise ValueError("no argument is given")
            lines = sys.stdin.readlines()
        elif len(args) == 1:
            file = args[-1]
            with open(file) as f:
                lines = f.readlines()
        else:
            raise ValueError("wrong command line argument number")

        lines = [line.strip() for line in lines]
        unique = [lines[0]] if lines else []
        for i in range(1, len(lines)):
            if lines[i] != lines[i - 1]:
                unique.append(lines[i])
        if self.__is_case_insensitive:
            unique_i = [unique[0]] if unique else []
            for i in range(1, len(unique)):
                if unique[i].lower() != unique[i - 1].lower():
                    unique_i.append(unique[i])
            unique = unique_i
        for line in unique:
            out.append(line + "\n")

    def __ignore_case_option(self):
        self.__is_case_insensitive = True


class Sort(Application):
    """Sorts the contents of a file/stdin line by line
    and prints the result to stdout

    The assumption of "-r" follows that,
    when sees a "-r", treat it as option,
    If there is a file "-r", use redirection or pipe"""

    def __init__(self):
        super().__init__()
        self.__options = {"-r": self.__reverse_order_option}
        self.__reverse_order = False

    def exec(self, args: Deque[str], out: Deque) -> None:
        while len(args) > 0 and args[0] in self.__options:
            self.__options[args.popleft()]()
        lines = []
        if len(args) == 0:
            if sys.stdin == sys.__stdin__:
                raise ValueError("no argument is given")
            lines = sys.stdin.readlines()
        elif len(args) == 1:
            file = args[-1]
            with open(file) as f:
                lines = f.readlines()
        else:
            raise ValueError("wrong command line argument number")

        lines = [line.strip() for line in lines]
        lines.sort()
        if self.__reverse_order:
            lines.sort(reverse=True)
        for line in lines:
            out.append(line + "\n")

    def __reverse_order_option(self):
        self.__reverse_order = True


class Exit(Application):
    """Exit shell with argument"""

    def __init__(self):
        super().__init__()

    def exec(self, args: Deque[str], out: Deque) -> None:
        if args and not args[0].isnumeric():
            raise ValueError("invalid exit code")
        print("=== Thank you for using COMP0010 Shell ===")
        out.append("")
        if len(args) == 0 or args[0] == "":
            exit(0)
        exit(int(args[0]))


class Cls(Application):
    """Clear screen method"""

    def __init__(self):
        super().__init__()

    def exec(self, args: Deque[str], out: Deque) -> None:
        os.system("cls" if os.name == "nt" else "clear")
        out.append("")


class ApplicationFactory:
    """The factory of Application Interface"""

    def __init__(self) -> None:
        self.__applications = {
            "pwd": Pwd,
            "cd": Cd,
            "echo": Echo,
            "ls": Ls,
            "cat": Cat,
            "head": Head,
            "tail": Tail,
            "grep": Grep,
            "cut": Cut,
            "find": Find,
            "uniq": Uniq,
            "sort": Sort,
            "exit": Exit,
            "cls": Cls,
        }

    def create_application(
        self, application_name: str, unsafe: bool = False
    ) -> Application:
        """Get an instance of concrete Application class.

        Args:
            application_name (str): The name of the application.
                                    If it is not supported by this module,
                                    an error will raise.
            unsafe (bool, optional): Defaults to False.
                                     If ture, this application is unsafe.

        Raises:
            ValueError: raised when the application is not supported.

        Returns:
            Application: The Application instance.
                         If unsafe is true,
                         the return type is UnsafeApplicationProxy,
                         a decorator of Application.
        """
        if application_name not in self.__applications.keys():
            raise ValueError(f"unsupported application {application_name}")
        application = self.__applications[application_name]()
        if unsafe:
            return UnsafeApplicationProxy(application)
        else:
            return application
