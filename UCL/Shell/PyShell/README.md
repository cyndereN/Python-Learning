# COMP0010 Shell

COMP0010 Shell is a [shell](https://en.wikipedia.org/wiki/Shell_(computing)) created for educational purposes. Similarly to other shells, it provides a [REPL](https://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop), an interactive environment that allows users to execute commands. COMP0010 Shell has a simple language for specifying commands that resembles [Bash](https://en.wikipedia.org/wiki/Bash_(Unix_shell)). This language allows, for example, calling applications and connecting the output of one application to the input of another application through a [pipeline](https://en.wikipedia.org/wiki/Pipeline_(Unix)). COMP0010 Shell also provides its own implementations of widely-used UNIX applications for file system and text manipulation: [echo](https://en.wikipedia.org/wiki/Echo_(command)), [ls](https://en.wikipedia.org/wiki/Ls), [cat](https://en.wikipedia.org/wiki/Cat_(Unix)), etc.  

In this project we have implemented all the features given in the requirement. We also add
a "cls" command that allows users to clear the command lines.   

For the interactive mode, we have modified it such that, 
if there is an error caused by users,
(e.g. wrong syntax, unsupported application and file not exist)
the program will not crash, but prints the error to stderr.
Users could exit the interactive mode by typing "exit [exit code]".
In the non-interactive mode, the error raised will not be handled.
unless users are using an unsafe application, e.g. _ls.


## Documentation

- [Language](doc/language.md)
- [Applications](doc/applications.md)
- [Command Line Interface](doc/interface.md)

## Prerequisites

- Python
- Docker

## Structure

```
|_ README.md
|_doc 
  |_ applications.md 
  |_ interface.md 
  |_ language.md
 
|_src  
  |_ shell.py 
  |_ applications.py
    |_ ls  
    |_ echo  
    |_...  
  |_ grammar.lark
  |_ converter.py
  |_ visitor.py
  |_ command.py
  |_ evaluator.py
|_system_test  
  |_ tests.py
|_test  
  |_ test_shell.py
|_ tools  
|_ Dockerfile  
|_ requirements.txt  
|_ sh  
```

## Contributors

[Ce Cao](<https://github.com/cyndereN>)  
[Leran Li](<https://github.com/Lokeyli>)  
[Yue He](<https://github.com/hiiamyue>)  

## References

- Design Patterns(Guru): (<https://refactoringguru.cn/design-patterns>)
- CS 61 Shell: (<https://cs61.seas.harvard.edu/site/2021/Shell/>)
- Cut: (<https://www.geeksforgeeks.org/cut-command-linux-examples/?ref=gcse>)
- Uniq: (<https://www.geeksforgeeks.org/uniq-command-in-linux-with-examples/?ref=gcse>)
- Stdin, out, err: (<https://book.51cto.com/art/201701/528133.htm>)
- Pipe, redirection: (<http://www.compciv.org/topics/bash/pipes-and-redirection/>)
- LARK: (<https://lark-parser.readthedocs.io/en/latest/>)
- Hypothesis: (https://hypothesis.readthedocs.io/en/latest/)
- Excluding code from coverage.py: (https://coverage.readthedocs.io/en/coverage-4.3.3/excluding.html#excluding-code-from-coverage-py)
- J. Vlissides, E. Gamma, R. Helm, and R. Johnson, "Discussion of Structural Patterns," in Design Patterns: Elements of Reusable Object-Oriented Software. Pearson Addison Wesley, 1994.
- pylint: (https://pylint.pycqa.org/en/latest/)
