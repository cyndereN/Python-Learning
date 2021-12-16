from typing import Deque
from abc import ABCMeta, abstractmethod
import sys
import os

from application_factory import ApplicationFactory


class Visitor(metaclass=ABCMeta):
    """Vistor Interface for Command Class"""

    @abstractmethod
    def visit_call(self, call, out):
        """Evaluates the Call instacnes"""
        pass

    @abstractmethod
    def visit_pipe(self, pipe, out):
        """Evaluates the Sequence instance"""
        pass

    @abstractmethod
    def visit_sequence(self, sequence, out):
        """Evaluates the Pipe instance."""
        pass


class Evaluator(Visitor):
    """Implements Visitor"""

    def visit_call(self, call, out: Deque) -> None:
        """Implementes the visit_call method in Visitor.

        Args:
            call (Call): The instance of Call to be evaluated
            out (Deque): The deque that holds the strings as output
        """
        origin_stdin, origin_stdout = sys.stdin, sys.stdout
        if call.stdin:
            sys.stdin = open(call.stdin, "r")
        if call.stdout:
            sys.stdout = open(call.stdout, "w")
        ApplicationFactory().create_application(
            call.application, call.is_unsafe
        ).exec(call.args, out)
        while len(out) > 0:
            print(out.popleft(), end="")
        if sys.stdin != origin_stdin:
            sys.stdin.close()
        if sys.stdout != origin_stdout:
            sys.stdout.close()
        sys.stdin, sys.stdout = origin_stdin, origin_stdout

    def visit_sequence(self, sequence, out: Deque) -> None:
        """Implementes the visit_sequence method in Visitor.

        Args:
            sequence (Sequence): The instance of Sequence to be evaluated
            out (Deque): The deque that holds the strings as output
        """
        for command in sequence.get_command_sequence():
            command.accept(self, out)

    def visit_pipe(self, pipe, out: Deque) -> None:
        """Implementes the visit_pipe method in Visitor.

        Before evaluates the calls of such pipe instance,
        this method reset the stdin to the previous pipe,
        and reset the stdout to the next pipe.
        Except for the first call and the last call.
        For the first call, only reset the stdout to its next pipe.
        For the last call, only reset the stdin to its previous pipe

        Args:
            pipe (Pipe): The instance of Pipe to be evaluated
            out (Deque): The deque that holds the strings as output
        """
        calls = pipe.get_commmand_pipe()
        origin_in, origin_out = sys.stdin, sys.stdout
        pipe_in, pipe_out = os.pipe()
        opened_pipe_out = open(pipe_out, "w")
        sys.stdout = opened_pipe_out
        calls[0].accept(self, out)
        opened_pipe_out.close()
        for call in calls[1:-1]:
            opened_pipe_in = open(pipe_in, "r")
            sys.stdin = opened_pipe_in
            pipe_in, pipe_out = os.pipe()
            opened_pipe_out = open(pipe_out, "w")
            sys.stdout = opened_pipe_out
            call.accept(self, out)
            opened_pipe_in.close()
            opened_pipe_out.close()
        sys.stdout = origin_out
        opened_pipe_in = open(pipe_in, "r")
        sys.stdin = opened_pipe_in
        calls[-1].accept(self, out)
        opened_pipe_in.close()
        sys.stdin = origin_in
