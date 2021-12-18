import unittest
import sys
import os
import re
import string
import subprocess
from pathlib import Path
from collections import deque

import hypothesis.strategies as st
from hypothesis import given, settings, example, assume, HealthCheck
from hypothesis.extra.lark import from_lark
from lark import Tree as larkTree

sys.path.append(str(Path(__file__).parent.resolve().with_name("src")))
import shell
from command import Command
from converter import CommandConverter, BackquoteDecorator
from evaluator import Evaluator

TEST_DEADLINE = 1000  # in ms, for parameter in hypothesis.setting.
TESTFILE_NUMBERS = "dirA/testfile1.txt"
TESTFILE_TEXT1 = "dirA/testfile2.txt"
TESTFILE_TEXT2 = "dirB/SUBdir/testfile1.txt"
TESTFILE_UNIQ = "dirA/testfile3.txt"


class TestShell(unittest.TestCase):

    backquote_parser = shell.get_parser("grammar.lark", "input_string")
    command_parser = shell.get_parser("grammar.lark", "command")

    @classmethod
    def setUpClass(cls) -> None:
        TestShell.command_converter = CommandConverter()
        TestShell.backquote_converter = BackquoteDecorator(
            TestShell.command_converter
        )
        TestShell.evaluator = Evaluator()
        TestShell.shell = shell.Shell(
            TestShell.backquote_parser,
            TestShell.command_parser,
            TestShell.backquote_converter,
            TestShell.command_converter,
            TestShell.evaluator,
        )
        TestShell.cwd = os.getcwd()

    def setUp(self) -> None:
        self.createDir()

    def createDir(self) -> None:
        init_cmd = (";").join(
            [
                "mkdir dirA",
                "mkdir dirB",
                "cd dirB",
                "mkdir SUBdir",
                "mkdir SUB",
                "cd ..",
                (";").join(
                    [f"echo {i} >> {TESTFILE_NUMBERS}" for i in range(0, 30)]
                ),
                'echo "Elephant\nDog\nHuman\nDog\nCat\nElephant"'
                + f"> {TESTFILE_TEXT1}",
                f'echo "London" > {TESTFILE_TEXT2}',
                f'echo "index test line" >> {TESTFILE_UNIQ}',
                (";").join(
                    [
                        f"echo '{chr(i) * 3}\n{chr(i) * 3}\n"
                        + f"{chr(i) * 3}\n{chr(i + 32) * 3}'"
                        + f">> {TESTFILE_UNIQ}"
                        for i in range(65, 65 + 26)  # ASCII, from A to Z
                    ]
                ),
                f'echo "index test line" >> {TESTFILE_UNIQ}',
            ]
        )
        subprocess.run(args=init_cmd, shell=True, cwd=TestShell.cwd)

    def tearDown(self) -> None:
        os.chdir(TestShell.cwd)
        # Reset, as some negative test will halt
        # before stdin/stdout is reset to the origin one
        self.reset_stdin_stdout()
        subprocess.run(
            args="rm -r dirA; rm -r dirB", shell=True, cwd=TestShell.cwd
        )

    def reset_stdin_stdout(self) -> None:
        if sys.stdin != sys.__stdin__:
            unclosed_resource = sys.stdin
            sys.stdin = sys.__stdin__
            unclosed_resource.close()
        if sys.stdout != sys.__stdout__:
            unclosed_resource = sys.stdout
            sys.stdout = sys.__stdout__
            unclosed_resource.close()

    def run_homegrown_shell(self, cmd: str) -> str:
        test_read, test_write = os.pipe()
        with open(test_write, "w") as shell_out:
            sys.stdout = shell_out
            TestShell.shell.eval(cmd, deque())
        sys.stdout = sys.__stdout__
        shell_out.close()
        out = None
        with open(test_read, "r") as test_in:
            out = test_in.readlines()
        test_in.close()
        return ("").join(out).strip()

    def run_default_shell(self, cmd: str) -> str:
        expected_out = subprocess.check_output(
            args=cmd, shell=True, cwd=TestShell.cwd
        )
        return expected_out.decode().strip()

    def count_max_redirection(self, cmd: str) -> int:
        commands = cmd.split(";")
        calls = []
        for command in commands:
            calls.extend(command.split("|"))
        num_of_redirection = 0
        for call in calls:
            if (
                call.count(">") > num_of_redirection
                or call.count("<") > num_of_redirection
            ):
                num_of_redirection = max(call.count(">"), call.count("<"))
        return num_of_redirection

    @given(from_lark(grammar=backquote_parser, start="input_string"))
    @settings(
        max_examples=20,
        deadline=TEST_DEADLINE,
        suppress_health_check=[
            HealthCheck.data_too_large
        ],  # from_lark does not have max_size parameter
    )
    def test_backquote_parser(self, cmd):
        syntax_tree = self.backquote_parser.parse(cmd)
        self.assertIsInstance(syntax_tree, larkTree)

    @given(from_lark(grammar=command_parser, start="command"))
    @settings(
        max_examples=20,
        deadline=TEST_DEADLINE,
        suppress_health_check=[
            HealthCheck.data_too_large
        ],  # from_lark does not have max_size parameter
    )
    def test_command_parser(self, cmd):
        syntax_tree = self.command_parser.parse(cmd)
        self.assertIsInstance(syntax_tree, larkTree)

    @given(from_lark(grammar=backquote_parser, start="input_string"))
    @settings(
        max_examples=20,
        deadline=TEST_DEADLINE,
        suppress_health_check=[
            HealthCheck.data_too_large
        ],  # from_lark does not have max_size parameter
    )
    @example("echo `cat < a.txt`")  # Valid
    @example("echo `cat < a.txt < b.txt`")  # Not valid stdin
    @example("cat `echo > a.txt > b.txt`")  # Not valid stdout
    def test_backquote_converter(self, cmd):
        syntax_tree = self.backquote_parser.parse(cmd)
        backquotes = re.findall(r"\`[^\`]*\`", cmd)
        max_redirections = max(
            [0] + [self.count_max_redirection(subcmd) for subcmd in backquotes]
        )  # backquote_converter only care about command inside a backquote
        if max_redirections <= 1:  # For an individual call,
            # only zero or one file should be specified for redirection.
            # converter should accept those cases.
            second_parse_input = self.backquote_converter.convert(syntax_tree)
            self.assertIsInstance(second_parse_input, list)
        else:  # Otherwise, the converter should throws exception.
            with self.assertRaisesRegex(
                IOError, "More than one file is specify for input/output."
            ):
                self.backquote_converter.convert(syntax_tree)

    @given(from_lark(grammar=command_parser, start="command"))
    @settings(
        max_examples=20,
        deadline=TEST_DEADLINE,
        suppress_health_check=[
            HealthCheck.data_too_large
        ],  # from_lark does not have max_size parameter
    )
    @example("cat < a.txt")  # Valid
    @example("cat < a.txt < b.txt")  # Not valid stdin
    @example("echo > a.txt > b.txt")  # Not valid stdout
    def test_command_converter(self, cmd):
        syntax_tree = self.command_parser.parse(cmd)
        if self.count_max_redirection(cmd) <= 1:  # For an individual call,
            # only zero or one file should be specified for redirection.
            # converter should accept those cases.
            command = self.command_converter.convert(syntax_tree)
            self.assertIsInstance(command, Command)
        else:  # Otherwise, the converter should throws exception.
            with self.assertRaisesRegex(
                IOError, "More than one file is specify for input/output."
            ):
                self.command_converter.convert(syntax_tree)

    @given(st.integers(min_value=1, max_value=10))
    @example(2)
    @example(3)
    @settings(deadline=TEST_DEADLINE)
    def test_pipe(self, num_of_commands):
        cmd = "echo test" + (" | ").join(
            ["cat" for i in range(0, num_of_commands)]
        )
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(expected_out, out)

    @given(st.integers(min_value=1, max_value=10))
    @example(2)
    @example(3)
    @settings(deadline=TEST_DEADLINE)
    def test_sequence(self, num_of_commands):
        cmd = (";").join(
            [f"echo test line {i}" for i in range(0, num_of_commands)]
        )
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(expected_out, out)

    @given(st.integers(min_value=1, max_value=10))
    @example(1)
    @settings(deadline=TEST_DEADLINE)
    def test_sequence_end_with_semicolon(self, num_of_commands):
        cmd = ("").join(
            [f"echo test line {i};" for i in range(0, num_of_commands)]
        )
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(expected_out, out)

    @given(st.integers(min_value=1, max_value=10))
    @example(1)
    @settings(deadline=TEST_DEADLINE)
    def test_sequence_with_pipe(self, num_of_commands):
        cmd = (";").join(
            [f"echo test line {i} | cat" for i in range(0, num_of_commands)]
        )
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(expected_out, out)

    def test_backquote(self):
        cmd = "echo `echo a`"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    def test_backquote_inside_singlequote(self):
        cmd = "echo '`echo a`'"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    def test_backquote_inside_doublequote(self):
        cmd = 'echo "`echo a`"'
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    def test_backquote_with_singlequote_inside(self):
        cmd = "echo `echo \"'a'\"`"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    def test_backquote_with_doublequote_inside(self):
        cmd = "echo `echo '\"a\"'`"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    def test_backquote_with_quote_inside_doublequote(self):
        cmd = 'echo "`echo "\'a\'"`"'
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    def test_no_space_in_quotes(self):
        cmd = 'echo unquoted1"in_quote1"unquoted2"in_quote2""in_quote3"'
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    def test_pwd(self):
        cmd = "pwd"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    def test_pwd_error_option_given(self):
        cmd = "pwd 33"
        with self.assertRaises(ValueError):
            self.run_homegrown_shell(cmd)

    def test_cd(self):
        cmd = "cd dirA ; pwd"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    def test_cd_error_option_given(self):
        cmd = "cd"
        with self.assertRaises(ValueError):
            self.run_homegrown_shell(cmd)

    def test_ls(self):
        cmd = "ls"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        out = set(out.split("\n"))
        expected_out = set(expected_out.split("\n"))
        self.assertEqual(out, expected_out)

    def test_ls_error_option_given(self):
        cmd = "ls dirA dirB"
        with self.assertRaises(
            ValueError,
        ):
            self.run_homegrown_shell(cmd)

    def test_ls_file(self):
        cmd = "ls dirA"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        out = set(out.split("\n"))
        expected_out = set(expected_out.split("\n"))
        self.assertEqual(out, expected_out)

    def test_cat(self):
        cmd = f"cat {TESTFILE_TEXT1} {TESTFILE_TEXT2}"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    def test_cat_stdin(self):
        cmd = f"cat < {TESTFILE_TEXT1}"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    def test_cat_error_no_file_args(self):
        cmd = "cat"
        with self.assertRaises(ValueError):
            self.run_homegrown_shell(cmd)

    @given(st.text(alphabet=string.ascii_letters, min_size=1))
    def test_echo(self, s):
        cmd = "echo {}".format(s)
        out = self.run_homegrown_shell(cmd)
        self.assertEqual(out, s)

    def test_head_option_free(self):
        cmd = f"head {TESTFILE_TEXT1}"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    @given(st.integers(min_value=1, max_value=10))
    def test_head_postive_non_zero_number(self, n):
        cmd = f"head -n {n} {TESTFILE_NUMBERS}"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    @given(st.integers(min_value=-10, max_value=0))
    @example(0)
    def test_head_error_invalid_number(self, n):
        cmd = f"head -n {n} {TESTFILE_NUMBERS}"
        with self.assertRaisesRegex(ValueError, f"illegal line count -- {n}"):
            self.run_homegrown_shell(cmd)

    def test_head_stdin(self):
        cmd = f"head -n 3 < {TESTFILE_NUMBERS}"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    @given(st.text(alphabet=string.ascii_letters, max_size=100))
    def test_head_error_not_number_line_value(self, n):
        cmd = f"head -n {n} {TESTFILE_NUMBERS}"
        with self.assertRaisesRegex(ValueError, f"illegal line count -- {n}"):
            self.run_homegrown_shell(cmd)

    def test_head_error_no_line_value(self):
        cmd = f"head -n < {TESTFILE_NUMBERS}"
        with self.assertRaisesRegex(
            ValueError, "option requires an argument -- n"
        ):
            self.run_homegrown_shell(cmd)

    def test_head_error_no_file_args(self):
        cmd = "head -n 3"
        with self.assertRaisesRegex(ValueError, "no argument is given"):
            self.run_homegrown_shell(cmd)

    def test_tail_option_free(self):
        cmd = f"tail {TESTFILE_TEXT1}"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    @given(st.integers(min_value=1, max_value=10))
    def test_tail_positive_non_zero_number(self, n):
        cmd = f"tail -n {n} {TESTFILE_NUMBERS}"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    @given(st.integers(min_value=-10, max_value=0))
    @example(0)
    def test_tail_error_invalid_number(self, n):
        cmd = f"tail -n {n} {TESTFILE_NUMBERS}"
        with self.assertRaisesRegex(ValueError, f"illegal line count -- {n}"):
            self.run_homegrown_shell(cmd)

    def test_tail_stdin(self):
        cmd = f"tail -n 3 < {TESTFILE_NUMBERS}"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    @given(st.text(alphabet=string.ascii_letters, max_size=100))
    def test_tail_error_not_number_line_value(self, n):
        cmd = f"tail -n {n} {TESTFILE_NUMBERS}"
        with self.assertRaisesRegex(ValueError, f"illegal line count -- {n}"):
            self.run_homegrown_shell(cmd)

    def test_tail_error_no_line_value(self):
        cmd = f"tail -n < {TESTFILE_NUMBERS}"
        with self.assertRaisesRegex(
            ValueError, "option requires an argument -- n"
        ):
            self.run_homegrown_shell(cmd)

    def test_tail_error_no_file_args(self):
        cmd = "tail -n 3"
        with self.assertRaisesRegex(ValueError, "no argument is given"):
            self.run_homegrown_shell(cmd)

    def test_grep_exact_word(self):
        cmd = f"grep Elephant {TESTFILE_TEXT1}"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    def test_grep_regex(self):
        cmd = f"grep Lon... {TESTFILE_TEXT2}"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    def test_grep_stdin(self):
        cmd = f"grep Cat < {TESTFILE_TEXT1}"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    def test_grep_no_match(self):
        cmd = f"grep apple {TESTFILE_NUMBERS}"
        out = self.run_homegrown_shell(cmd)
        self.assertEqual(out, "")

    def test_grep_multiple_files(self):
        cmd = f"grep '....' {TESTFILE_TEXT1} {TESTFILE_TEXT2}"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    def test_grep_error_no_args(self):
        cmd = "grep"
        with self.assertRaises(ValueError):
            self.run_homegrown_shell(cmd)

    def test_grep_error_no_file_args(self):
        cmd = "grep '....'"
        with self.assertRaises(ValueError):
            self.run_homegrown_shell(cmd)

    def test_grep_error_no_pattern(self):
        cmd = f"grep < {TESTFILE_TEXT1}"
        with self.assertRaises(ValueError):
            self.run_homegrown_shell(cmd)

    @given(
        x=st.integers(min_value=1, max_value=10),
        y=st.integers(min_value=1, max_value=10),
        z=st.integers(min_value=1, max_value=10),
    )
    def test_cut_exactly(self, x, y, z):
        cmd = f"cut -b {x},{y},{z} {TESTFILE_TEXT1}"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    @given(
        x=st.integers(min_value=1, max_value=10),
        y=st.integers(min_value=1, max_value=10),
        z=st.integers(min_value=1, max_value=10),
    )
    def test_cut_stdin(self, x, y, z):
        cmd = f"cut -b {x},{y},{z} < {TESTFILE_TEXT1}"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    @given(
        x=st.integers(min_value=1, max_value=10),
        y=st.integers(min_value=1, max_value=10),
        z=st.integers(min_value=1, max_value=10),
        w=st.integers(min_value=1, max_value=10),
    )
    def test_cut_range(self, x, y, z, w):
        # some shell (e.g. zsh) allow decreasing range, our shell follows this.
        assume(x <= y and z <= w)
        cmd = f"cut -b {x}-{y},{z}-{w} {TESTFILE_TEXT1}"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    def test_cut_decreasing_range(self):
        cmd = f"cut -b 2-1,3-2 {TESTFILE_TEXT1}"
        out = self.run_homegrown_shell(cmd)
        self.assertEqual(out, "")

    @given(
        x=st.integers(min_value=1, max_value=10),
        y=st.integers(min_value=1, max_value=10),
    )
    def test_cut_open_interval(self, x, y):
        cmd = f"cut -b -{x},{y}- {TESTFILE_TEXT1}"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    def test_cut_error_no_option_given(self):
        cmd = f"cut {TESTFILE_TEXT1}"
        with self.assertRaisesRegex(
            ValueError, "usage: cut -b list \\[file ...\\]"
        ):
            self.run_homegrown_shell(cmd)

    def test_cut_error_no_args_given_to_option(self):
        cmd = f"cut -b < {TESTFILE_TEXT1}"
        with self.assertRaisesRegex(
            ValueError, "option requires an argument -- b"
        ):
            self.run_homegrown_shell(cmd)

    def test_cut_error_no_file_args_given(self):
        cmd = "cut -b 1,2,3"
        with self.assertRaisesRegex(ValueError, "no argument is given"):
            self.run_homegrown_shell(cmd)

    def test_cut_error_non_numeric_args_given_to_option(self):
        cmd = f"cut -b a,b,c {TESTFILE_TEXT1}"
        with self.assertRaisesRegex(ValueError, "illegal list count"):
            self.run_homegrown_shell(cmd)

    def test_cut_error_zero_given_to_option_in_range(self):
        # a range with no number on both consider as zero
        cmd = f"cut -b - {TESTFILE_TEXT1}"
        with self.assertRaisesRegex(ValueError, "values may not include zero"):
            self.run_homegrown_shell(cmd)

    def test_cut_error_zero_given_to_option_exactly(self):
        cmd = f"cut -b 0 {TESTFILE_TEXT1}"
        with self.assertRaisesRegex(ValueError, "values may not include zero"):
            self.run_homegrown_shell(cmd)

    def test_cut_error_wrong_range_format(self):
        cmd = f"cut -b 1-2-3 {TESTFILE_TEXT1}"
        with self.assertRaisesRegex(ValueError, "illegal list count"):
            self.run_homegrown_shell(cmd)

    def test_find(self):
        cmd = "find -name testfile2.txt"
        out = self.run_homegrown_shell(cmd)
        self.assertEqual(out, f"./{TESTFILE_TEXT1}")

    def test_find_glob(self):
        cmd = "find -name testfile*"
        out = set(self.run_homegrown_shell(cmd).split("\n"))
        self.assertEqual(
            out,
            set(
                [
                    f"./{TESTFILE_TEXT2}",
                    f"./{TESTFILE_TEXT1}",
                    f"./{TESTFILE_NUMBERS}",
                    f"./{TESTFILE_UNIQ}",
                ]
            ),
        )

    def test_find_error_no_args(self):
        cmd = "find"
        with self.assertRaises(ValueError):
            self.run_homegrown_shell(cmd)

    def test_find_error_wrong_option(self):
        cmd2 = " find dirA -x *"
        with self.assertRaises(ValueError):
            self.run_homegrown_shell(cmd2)

    def test_uniq(self):
        cmd = f"uniq {TESTFILE_UNIQ}"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    def test_uniq_stdin(self):
        cmd = f"uniq < {TESTFILE_UNIQ}"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    def test_uniq_case_insensitive_option(self):
        cmd = f"uniq -i {TESTFILE_UNIQ}"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    def test_uniq_error_more_than_one_file_args(self):
        cmd = f"uniq {TESTFILE_UNIQ} {TESTFILE_NUMBERS}"
        with self.assertRaises(ValueError):
            self.run_homegrown_shell(cmd)

    def test_uniq_error_no_file_args(self):
        cmd1 = "uniq"
        with self.assertRaises(ValueError):
            self.run_homegrown_shell(cmd1)

    def test_sort(self):
        cmd = f"sort {TESTFILE_TEXT1}"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    def test_sort_option_r(self):
        cmd = f"sort -r {TESTFILE_TEXT1}"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    def test_sort_stdin(self):
        cmd = f"sort < {TESTFILE_TEXT1}"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    def test_sort_error_more_than_one_file_args(self):
        cmd = f"sort -r {TESTFILE_NUMBERS} {TESTFILE_TEXT1}"
        with self.assertRaises(ValueError):
            self.run_homegrown_shell(cmd)

    def test_sort_error_no_file_args(self):
        cmd = "sort"
        with self.assertRaises(ValueError):
            self.run_homegrown_shell(cmd)

    def test_sort_error_file_wrong_option(self):
        cmd = f"sort -n {TESTFILE_NUMBERS}"
        with self.assertRaises(ValueError):
            self.run_homegrown_shell(cmd)

    def test_ls_unsafe(self):
        cmd = f"ls dirB; echo BBB > {TESTFILE_TEXT2}"
        self.run_homegrown_shell(cmd)
        out = self.run_homegrown_shell(f"cat {TESTFILE_TEXT2}")
        expected_out = self.run_default_shell(f"cat {TESTFILE_TEXT2}")
        self.assertEqual(out, expected_out)

    def test_exit(self):
        cmd = "exit"
        with self.assertRaises(SystemExit):
            self.run_homegrown_shell(cmd)

    def test_exit_error_option_given(self):
        cmd = "exit 1"
        with self.assertRaises(SystemExit):
            self.run_homegrown_shell(cmd)

    def test_exit_error_option_args_not_numeric(self):
        cmd = "exit asdf"
        with self.assertRaises(ValueError):
            self.run_homegrown_shell(cmd)

    def test_wrongappilication(self):
        cmd = "dance"
        with self.assertRaises(ValueError):
            self.run_homegrown_shell(cmd)

    def test_unsafe_call(self):
        cmd = "_echo 123"
        out = self.run_homegrown_shell(cmd)
        expected_out = "[Proxy: Logging unsafe mode.]123"
        self.assertEqual(out, expected_out)

    def test_unsafe_seq(self):
        cmd = "_pwd 123 ; echo 123"
        out = self.run_homegrown_shell(cmd)
        out_without_error_message = ("").join(out.split("\n")[1:])
        expected_out = "123"
        self.assertEqual(out_without_error_message, expected_out)


if __name__ == "__main__":
    unittest.main()
