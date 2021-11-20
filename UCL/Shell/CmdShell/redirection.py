import os
import sys

inputs = input('$ ').split('<')
command = inputs[0].strip().split()
file = None
if len(inputs) == 2:
    file = inputs[1].strip()
child_pid = os.fork()
if child_pid == 0:
    if file is not None:
        fd = os.open(file, os.O_RDONLY)
        os.dup2(fd, sys.stdin.fileno())
    os.execvp(command[0], command)
else:
    os.waitpid(child_pid, 0)