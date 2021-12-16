import unittest
import sys
import os
import re
import string
import subprocess
from pathlib import Path, PurePath
from collections import deque

import hypothesis.strategies as st
from hypothesis import *
from hypothesis.extra.lark import from_lark
from lark import Tree as larkTree

sys.path.append(str(Path(__file__).parent.resolve().with_name("src")))
import shell
from command import Command
from converter import CommandConverter, BackquoteDecorator
from evaluator import Evaluator


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

    def count_max_redirection(self, cmd):
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

    def setUp(self):
        self.createDir()

    def tearDown(self) -> None:
        os.chdir(TestShell.cwd)
        subprocess.run(
            args="rm -r dirA; rm -r dirB", shell=True, cwd=TestShell.cwd
        )

    def run_homegrown_shell(self, cmd):
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

    def run_default_shell(self, cmd):
        expected_out = subprocess.check_output(
            args=cmd, shell=True, cwd=TestShell.cwd
        )
        return expected_out.decode().strip()

    def createDir(self):
        init_cmd = (";").join(
            [
                "mkdir dirA",
                "mkdir dirB",
                "cd dirB",
                "mkdir SUBdir",
                "mkdir SUB",
                "cd ..",
                "echo 0 > dirA/testfile1.txt",
                (";").join(
                    [f"echo {i} >> dirA/testfile1.txt" for i in range(1, 30)]
                ),
                'echo "Elephant\nDog\nHuman\nDog\nCat\nElephant" > dirA/testfile2.txt',
                'echo "London" > dirB/SUBdir/testfile1.txt',
            ]
        )
        subprocess.run(args=init_cmd, shell=True, cwd=TestShell.cwd)

    @given(st.text(alphabet=string.ascii_letters, min_size=1))
    def test_Echo(self, s):
        cmd = "echo {}".format(s)
        out = self.run_homegrown_shell(cmd)
        self.assertEqual(out, s)

    def test_pwd(self):
        cmd = "pwd"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    def test_cd(self):
        cmd = "cd dirA ; pwd"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    def test_ls(self):
        cmd = "ls"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        out = set(out.split("\n"))
        expected_out = set(expected_out.split("\n"))
        self.assertEqual(out, expected_out)

    def test_ls_file(self):
        cmd = "ls dirA"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        out = set(out.split("\n"))
        expected_out = set(expected_out.split("\n"))
        self.assertEqual(out, expected_out)

    def test_cat(self):
        cmd = "cat dirA/testfile2.txt dirB/SUBdir/testfile1.txt"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    def test_cat_stdin(self):
        cmd = "cat < dirA/testfile2.txt"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    def test_head_no_number_specify(self):
        cmd = "head dirA/testfile2.txt"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    @given(st.integers(min_value=-pow(2, 20), max_value=pow(2, 20)))
    @example(-10)
    @example(0)
    @example(10)
    def test_head_any_number(self, n):
        cmd = f"head -n {n} dirA/testfile1.txt"
        if n > 0:
            out = self.run_homegrown_shell(cmd)
            expected_out = self.run_default_shell(cmd)
            self.assertEqual(out, expected_out)
        else:
            with self.assertRaises(ValueError):
                self.run_homegrown_shell(cmd)

    @given(st.text(alphabet=string.ascii_letters, max_size=100))
    def test_head_not_number_line_value(self, n):
        cmd = f"head -n {n} dirA/testfile1.txt"
        with self.assertRaises(ValueError):
            self.run_homegrown_shell(cmd)

    def test_tail_no_number_specified(self):
        cmd = f"tail dirA/testfile2.txt"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    @given(st.integers(min_value=-pow(2, 20), max_value=pow(2, 20)))
    @example(-10)
    @example(0)
    @example(10)
    def test_tail_any_number(self, n):
        cmd = f"tail -n {n} dirA/testfile1.txt"
        if n > 0:
            out = self.run_homegrown_shell(cmd)
            expected_out = self.run_default_shell(cmd)
            self.assertEqual(out, expected_out)
        else:
            with self.assertRaises(ValueError):
                self.run_homegrown_shell(cmd)

    @given(st.text(alphabet=string.ascii_letters, max_size=100))
    def test_tail_not_number_line_value(self, n):
        cmd = f"tail -n {n} dirA/testfile1.txt"
        with self.assertRaises(ValueError):
            self.run_homegrown_shell(cmd)

    def test_grep(self):
        cmd = "grep Elephant dirA/testfile2.txt"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    def test_grep_2(self):
        cmd = "grep Lon... dirB/SUBdir/testfile1.txt"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    def test_grep_stdin(self):
        cmd = "grep Cat < dirA/testfile2.txt"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    def test_grep_noMatch(self):
        cmd = "grep apple dirA/testfile1.txt"
        out = self.run_homegrown_shell(cmd)
        self.assertEqual(out, "")

    def test_grep_file(self):
        cmd = "grep '....' dirA/testfile2.txt dirB/SUBdir/testfile1.txt"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    def test_cut(self):
        cmd = "cut -b 1,2,3 dirA/testfile2.txt "
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    def test_cut_range(self):
        cmd = "cut -b 1-3,5-7 dirA/testfile2.txt "
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    def test_cut_range2(self):
        cmd = "cut -b -3,5- dirA/testfile2.txt "
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    def test_find(self):
        cmd = "find -name testfile2.txt"
        out = self.run_homegrown_shell(cmd)
        self.assertEqual(out, "./dirA/testfile2.txt")

    def test_find_pattern(self):
        cmd = "find -name testfile*"
        out = self.run_homegrown_shell(cmd)
        self.assertEqual(
            out,
            "./dirB/SUBdir/testfile1.txt\n./dirA/testfile2.txt\n./dirA/testfile1.txt",
        )

    def test_uniq(self):
        cmd = "echo Human > dirA/testfile2.txt"
        cmd = "uniq dirA/testfile2.txt"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    def test_uniq_case(self):
        cmd = "uniq -i dirA/testfile2.txt"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    def test_sort(self):
        cmd = "sort dirA/testfile2.txt"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    def test_sort_r(self):
        cmd = "sort -r dirA/testfile2.txt"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    def test_ls_unsafe(self):
        cmd = "ls dirB; echo BBB > dirB/SUBdir/testfile1.txt"
        self.run_homegrown_shell(cmd)
        out = self.run_homegrown_shell("cat dirB/SUBdir/testfile1.txt")
        expected_out = self.run_default_shell("cat dirB/SUBdir/testfile1.txt")
        self.assertEqual(out, expected_out)

    def test_uniq_pipe(self):
        cmd = "cat  dirB/SUBdir/testfile1.txt | uniq -i"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    def test_exit(self):
        cmd = "exit"
        with self.assertRaises(SystemExit):
            self.run_homegrown_shell(cmd)

    def test_cls(self):
        with self.assertRaisesRegex(
            ValueError, "wrong number of command line arguments"
        ):
            cmd = "cls x"
            self.run_homegrown_shell(cmd)
            sys.argv = ""

    def test_echo_back(self):
        cmd = "echo `echo a`"
        out = self.run_homegrown_shell(cmd)
        expected_out = self.run_default_shell(cmd)
        self.assertEqual(out, expected_out)

    def test_shell(self):
        with self.assertRaises(ValueError):
            shell.main()

    def test_wrongappilication(self):
        cmd = "dance"
        with self.assertRaises(ValueError):
            self.run_homegrown_shell(cmd)

    def test_pwd_error(self):
        cmd = "pwd 33"
        with self.assertRaises(ValueError):
            self.run_homegrown_shell(cmd)

    def test_cd_error(self):
        cmd = "cd"
        with self.assertRaises(ValueError):
            self.run_homegrown_shell(cmd)

    def test_ls_error(self):
        cmd = "ls dirA dirB"
        with self.assertRaises(
            ValueError,
        ):
            self.run_homegrown_shell(cmd)

    def test_cat_error(self):
        cmd = "cat"
        with self.assertRaises(ValueError):
            self.run_homegrown_shell(cmd)

    def test_head_error(self):
        cmd = "head"
        with self.assertRaises(ValueError):
            self.run_homegrown_shell(cmd)

        cmd2 = "head -n"
        with self.assertRaises(ValueError):
            self.run_homegrown_shell(cmd2)

        cmd3 = " head -n 15 "
        with self.assertRaises(ValueError):
            self.run_homegrown_shell(cmd3)

        cmd4 = "head -n -1"
        with self.assertRaises(ValueError):
            self.run_homegrown_shell(cmd4)

    def test_tail_error(self):
        cmd = "tail"
        with self.assertRaises(ValueError):
            self.run_homegrown_shell(cmd)

        cmd2 = "tail -n"
        with self.assertRaises(ValueError):
            self.run_homegrown_shell(cmd2)

        cmd4 = "tail -n -1"
        with self.assertRaises(ValueError):
            self.run_homegrown_shell(cmd4)

    def test_grep_error(self):
        cmd = "grep"
        with self.assertRaises(ValueError):
            self.run_homegrown_shell(cmd)
        cmd2 = "grep test.txt"
        with self.assertRaises(ValueError):
            self.run_homegrown_shell(cmd2)

    def test_cut_error(self):
        cmd = "cut"
        with self.assertRaises(ValueError):
            self.run_homegrown_shell(cmd)

    def test_find_error(self):
        cmd = "find "
        with self.assertRaises(ValueError):
            self.run_homegrown_shell(cmd)
        cmd2 = " find dirA -x *"
        with self.assertRaises(ValueError):
            self.run_homegrown_shell(cmd2)

    def test_uniq_error(self):
        cmd = "uniq -i dirA aa"
        with self.assertRaises(ValueError):
            self.run_homegrown_shell(cmd)
        cmd1 = "uniq"
        with self.assertRaises(ValueError):
            self.run_homegrown_shell(cmd1)
        cmd2 = "uniq -a file"
        with self.assertRaises(ValueError):
            self.run_homegrown_shell(cmd2)
        cmd3 = "uniq -i  "
        with self.assertRaises(ValueError):
            self.run_homegrown_shell(cmd3)

    def test_sort_error(self):
        cmd = "sort -r file file2"
        with self.assertRaises(ValueError):
            self.run_homegrown_shell(cmd)
        cmd1 = "sort"
        with self.assertRaises(ValueError):
            self.run_homegrown_shell(cmd1)
        cmd2 = "sort -n xx.txt"
        with self.assertRaises(ValueError):
            self.run_homegrown_shell(cmd2)
        cmd3 = "sort -r"
        with self.assertRaises(ValueError):
            self.run_homegrown_shell(cmd3)

    @given(from_lark(grammar=backquote_parser, start="input_string"))
    @settings(
        max_examples=20,
        deadline=1000,
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
        deadline=1000,
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
        deadline=1000,
        suppress_health_check=[
            HealthCheck.data_too_large
        ],  # from_lark does not have max_size parameter
    )
    @example("echo `cat < a.txt`")  # Valid
    @example("echo `cat < a.txt < b.txt`")  # Not valid
    def test_backquote_converter(self, cmd):
        syntax_tree = self.backquote_parser.parse(cmd)
        backquotes = re.findall(r"\`[^\`]*\`", cmd)
        max_redirections = max(
            [0] + [self.count_max_redirection(subcmd) for subcmd in backquotes]
        )  # backquote_converter only care about command inside a backquote
        if max_redirections <= 1:  # For a individual call,
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
        deadline=1000,
        suppress_health_check=[
            HealthCheck.data_too_large
        ],  # from_lark does not have max_size parameter
    )
    @example("cat < a.txt")  # Valid
    @example("cat < a.txt < b.txt")  # Not valid
    def test_command_converter(self, cmd):
        syntax_tree = self.command_parser.parse(cmd)
        if self.count_max_redirection(cmd) <= 1:  # For a individual call,
            # only zero or one file should be specified for redirection.
            # converter should accept those cases.
            command = self.command_converter.convert(syntax_tree)
            self.assertIsInstance(command, Command)
        else:  # Otherwise, the converter should throws exception.
            with self.assertRaisesRegex(
                IOError, "More than one file is specify for input/output."
            ):
                self.command_converter.convert(syntax_tree)


if __name__ == "__main__":
    unittest.main()
