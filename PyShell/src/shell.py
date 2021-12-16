import sys
import os
from collections import deque
from pathlib import Path
from typing import Deque

from lark import Lark

from converter import CommandConverter, BackquoteDecorator, Converter
from evaluator import Evaluator
from command import Command


class Shell:
    def __init__(
        self,
        backquote_parser: Lark,
        command_parser: Lark,
        backquote_converter: Converter,
        command_converter: Converter,
        evaluator: Evaluator,
    ) -> None:
        self.backquote_parser: Lark = backquote_parser
        self.command_parser: Lark = command_parser
        self.backquote_converter: Converter = backquote_converter
        self.command_converter: Converter = command_converter
        self.evaluator: Evaluator = evaluator

    def eval(self, cmdline: str, out: Deque):
        """Carry the corresponding operation form the cmdline input"""
        command: Command = self._convert(cmdline)
        command.accept(self.evaluator, out)

    def _convert(self, cmdline: str):
        """Parse the input cmdline.

        This method will parse the input string twice.
        Assume the input string is valid.
        The first time, it will find out all the backquote and evaluates it,
        then, return a string for second parsing.
        The second parsing which will return a command instance.
        If the input string has syntax error, this method will not handle it.

        Args:
            cmdline (str): The input string from user.

        Returns:
            command (Command): the corresponding command instance.
        """
        cmdline_without_backquote: str = self._first_parse(cmdline)
        command: Command = self._second_parse(cmdline_without_backquote)
        return command

    def _first_parse(self, cmdline: str):
        """Parser the cmdline to solve the backquote

        Args:
            cmdline (str): The input directly gets from user

        Returns:
            str: The return string as input for the second parse
        """

        second_parse_input: str = ""
        first_parse_tree = self.backquote_parser.parse(cmdline)
        first_ast = self.backquote_converter.convert(first_parse_tree)
        for node in first_ast:
            if not isinstance(node, str):
                origin_in, origin_out = sys.stdin, sys.stdout
                tmp_in, tmp_out = os.pipe()
                opened_pipe_out = open(tmp_out, "w")
                sys.stdout = opened_pipe_out
                node.accept(self.evaluator, deque())
                opened_pipe_out.close()
                sys.stdout = origin_out
                opened_pipe_in = open(tmp_in, "r")
                sys.stdin = opened_pipe_in
                tmp_str = ("").join(sys.stdin.read())
                opened_pipe_in.close()
                sys.stdin = origin_in
                if tmp_str.endswith("\n"):
                    tmp_str = tmp_str[:-1].replace("\n", " ")
                    double_quote_count = second_parse_input.count('"')
                    if double_quote_count % 2 == 1:
                        # backquote inside the double quote
                        second_parse_input += tmp_str.replace('"', '"\'"\'"')
                    else:
                        second_parse_input += (
                            tmp_str.replace("'", "\\'")
                            .replace('"', '\\"')
                            .replace("\\'", '"\'"')
                            .replace('\\"', "'\"'")
                        )
            else:
                second_parse_input += node
        second_parse_input = second_parse_input.replace("\n", " ")
        return second_parse_input

    def _second_parse(self, cmdline_without_backquote: str):
        """Parse again and get the command

        Args:
            cmdline_without_backquote (str):  the cmdline without backquote

        Returns:
            [type]: the Command instance from the given cmdline
        """
        second_parse_tree = self.command_parser.parse(
            cmdline_without_backquote
        )
        command: Command = self.command_converter.convert(second_parse_tree)
        return command


def get_parser(
    filename: str, strat_rule: str, parsing_method: str = "earley"
) -> Lark:
    """Get the lark parser from the given parameters.

    Args:
        filename (str): The name of the grammar file
        strat_rule (str): The name of the strat rule of such grammar
        parsing_method (str, optional): The parser is going to use.
            Defaults to "earley".

    Returns:
        Lark: The lark parser. Has parse() method for parsing.
    """
    with open(Path(__file__).with_name(filename), encoding="utf-8") as grammar:
        return Lark(
            grammar=grammar,
            start=strat_rule,
            parser=parsing_method,
        )


def main():
    backquote_parser = get_parser("grammar.lark", "input_string")
    command_parser = get_parser("grammar.lark", "command")
    command_converter = CommandConverter()
    backquote_converter = BackquoteDecorator(command_converter)
    evaluator = Evaluator()
    shell = Shell(
        backquote_parser,
        command_parser,
        backquote_converter,
        command_converter,
        evaluator,
    )
    args_num = len(sys.argv) - 1
    if args_num > 0:
        if args_num != 2:
            raise ValueError("wrong number of command line arguments")
        if sys.argv[1] != "-c":
            raise ValueError(f"unexpected command line argument {sys.argv[1]}")
        out = deque()
        shell.eval(sys.argv[2], out)
    else:
        print("==== Welcome to COMP0010 Shell ====")
        while True:
            print(os.getcwd() + "> ", end="")
            cmdline = input()
            out = deque()
            shell.eval(cmdline, out)


if __name__ == "__main__":
    main()
