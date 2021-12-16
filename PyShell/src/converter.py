from typing import List
from abc import ABCMeta, abstractmethod
from collections import deque

from lark import Tree, Token
from lark.visitors import Interpreter

from command import Command, Call, Sequence, Pipe


class Converter(Interpreter, metaclass=ABCMeta):
    """Translate the parse tree to AST"""

    def __init__(self) -> None:
        pass

    def _get_tokens(self, tree: Tree) -> List[str]:
        """Gets all the tokens from this given tree

        Args:
            tree (Tree): The node that contains token(s)

        Returns:
            [str]: A list of token(s)
        """
        token_generator = tree.scan_values(
            lambda token: isinstance(token, Token)
        )
        return [token.value for token in token_generator]

    @abstractmethod
    def convert(self, tree: Tree):
        pass


class CommandConverter(Converter):
    def __init__(self) -> None:
        super().__init__()

    def convert(self, tree: Tree) -> Command:
        """Convert the parse tree to AST

        Args:
            tree (Tree): the whole parse tree from the parser

        Returns:
            (Command): A instance of command
        """
        return self.visit(tree)

    """Convert to the AST from section Command Line in grammar.lark"""

    def command(self, tree: Tree):
        return self.visit(tree.children[0])

    def call(self, tree: Tree):
        call = Call()
        for child in tree.children:
            if child.data == "application_call":
                self._set_up_call(child, call)
            else:
                self._set_up_redirection(child, call)
        return call

    def _set_up_call(self, tree: Tree, call: Call):
        call.application, call.is_unsafe = self.visit(tree.children[0])
        for child in tree.children[1:]:
            call.args = self.visit(child)

    def _set_up_redirection(self, tree: Tree, call: Call):
        if tree.data == "input_redirection":
            if call.stdin:
                raise IOError(
                    "More than one file is specify for input/output."
                )
            else:
                call.stdin = ("").join(self.visit(tree))
        else:
            if call.stdout:
                raise IOError(
                    "More than one file is specify for input/output."
                )
            call.stdout = ("").join(self.visit(tree))

    def pipe(self, tree: Tree):
        pipe: Pipe = Pipe(self.visit(tree.children[0]))
        self._append_pipe(tree.children[1], pipe)
        return pipe

    def _append_pipe(self, tree: Tree, pipe: Pipe):
        if tree.data == "call":
            pipe.add_command(self.visit(tree))
        else:
            pipe.add_command(self.visit(tree.children[0]))
            self._append_pipe(tree.children[1], pipe)

    def seq(self, tree: Tree):
        sequence: Sequence = Sequence(self.visit(tree.children[0]))
        self._append_sequence(tree.children[1], sequence)
        return sequence

    def _append_sequence(self, tree: Tree, sequence: Sequence):
        if tree.data != "seq":
            sequence.add_command(self.visit(tree))
        else:
            sequence.add_command(self.visit(tree.children[0]))
            self._append_sequence(tree.children[1], sequence)

    """Convert to the AST from section Quoting in grammar.lark"""

    def single_quote(self, tree: Tree):
        return super()._get_tokens(tree)

    def double_quote(self, tree: Tree):
        return super()._get_tokens(tree)

    def quote_no_space(self, tree: Tree):
        tokens = []
        for subtree in tree.children:
            tokens += self.visit(subtree)
        return ("").join(tokens)

    """Convert to the AST from section Call Command in grammar.lark"""

    def application(self, tree: Tree):
        application_name = super()._get_tokens(tree).pop()
        return application_name, False

    def unsafe_application(self, tree: Tree):
        application_name = super()._get_tokens(tree).pop()
        return application_name, True

    def arguments(self, tree: Tree):
        arguments = deque()
        for sub_tree in tree.children:
            argument = self.visit(sub_tree)
            if isinstance(argument, list):
                arguments += argument
            else:
                arguments.append(argument)
        return arguments

    def unquoted(self, tree: Tree):
        return super()._get_tokens(tree)

    def input_redirection(self, tree: Tree):
        return super()._get_tokens(tree)

    def output_redirection(self, tree: Tree):
        return super()._get_tokens(tree)


class ConverterDecorator(Converter, metaclass=ABCMeta):
    def __init__(self, converter: Converter) -> None:
        self._converter: Converter = converter

    def convert(self, tree: Tree):
        return self._converter.convert(tree)


class BackquoteDecorator(ConverterDecorator):
    def __init__(self, converter: Converter) -> None:
        super().__init__(converter)

    def convert(self, tree: Tree) -> List:
        """Convert the parse tree to AST for the first parse

        Args:
            tree (Tree): the whole parse tree from the parser

        Returns:
            (List): The list of string and Command
        """
        return self.visit(tree)

    def input_string(self, tree: Tree):
        tokens = []
        for sub_tree in tree.children:
            tokens.append(self.visit(sub_tree))
        return tokens

    def other(self, tree: Tree):
        return ("").join(super()._get_tokens(tree))

    def single_quote_in_first_parse(self, tree: Tree):
        return ("").join(super()._get_tokens(tree))

    def backquote(self, tree: Tree):
        return self._converter.convert(tree.children[0])

    def empty_backquote(self, tree: Tree):
        return ""
