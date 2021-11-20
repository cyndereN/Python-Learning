import os
import sys

args1, args2 = input('$ ').split('|')
command1 = args1.split()
command2 = args2.split()
fd_for_read, fd_for_write = os.pipe()
child_1 = os.fork()
if child_1 == 0:  # 我们指定管道左端的程序为child_1
    os.dup2(fd_for_write, sys.stdout.fileno())  # 让左端程序的输出与管道的写入端连接
    os.close(fd_for_read)  # 关闭左端程序中不需要的管道接口
    os.execvp(command1[0], command1)  # 执行左端的程序
else:
    child_2 = os.fork()
    if child_2 == 0:  # 右端的程序为child_2
        os.dup2(fd_for_read, sys.stdin.fileno())  # 让右端程序的输入与管道的输出端连接
        os.close(fd_for_write)  # 关闭右端程序中不需要的管道接口
        os.execvp(command2[0], command2)  # 执行右端的程序
    else:
        os.waitpid(child_1, 0)
        os.waitpid(child_2, 0)