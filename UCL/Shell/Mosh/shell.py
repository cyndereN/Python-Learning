import sys
import shlex
import os
from Mosh.constants import *
#from Mosh.builtins import *
from Mosh.builtins.cd import *
from Mosh.builtins.exit import *

### 使用哈希映射来存储内建的函数名及其引用
built_in_cmds = {}

### 注册内建函数到内建命令的哈希映射中
def register_command(name, func):
    built_in_cmds[name] = func

### 在此注册所有的内建命令
def init():
    register_command("cd", cd)
    register_command("exit", exit)

def tokenize(string):
    return shlex.split(string)


def shell_loop():
    # Start the loop here
    status = SHELL_STATUS_RUN

    while status == SHELL_STATUS_RUN:
        ### 显示命令提示符
        sys.stdout.write('> ')
        sys.stdout.flush()
        ### 读取命令输入
        cmd = sys.stdin.readline()

        ### 切分命令输入
        cmd_tokens = tokenize(cmd)
        ### 执行该命令并获取新的状态
        status = execute(cmd_tokens)

def execute(cmd_tokens):
    ### 从元组中分拆命令名称与参数
    cmd_name = cmd_tokens[0]
    cmd_args = cmd_tokens[1:]
    ### 如果该命令是一个内建命令，使用参数调用该函数
    if cmd_name in built_in_cmds:
        return built_in_cmds[cmd_name](cmd_args)
    ### 分叉一个子 shell 进程
    ### 如果当前进程是子进程，其 `pid` 被设置为 `0`
    ### 否则当前进程是父进程的话，`pid` 的值
    ### 是其子进程的进程 ID。
    pid = os.fork()
    if pid == 0:
    ### 子进程
        ### 用被 exec 调用的程序替换该子进程
        os.execvp(cmd_tokens[0], cmd_tokens)
    elif pid > 0:
    ### 父进程
        while True:
            ### 等待其子进程的响应状态（以进程 ID 来查找）
            wpid, status = os.waitpid(pid, 0)
            ### 当其子进程正常退出时
            ### 或者其被信号中断时，结束等待状态
            if os.WIFEXITED(status) or os.WIFSIGNALED(status):
                break
    ### 返回状态以告知在 shell_loop 中等待下一个命令
    return SHELL_STATUS_RUN

def main():
    init()
    shell_loop()


if __name__ == "__main__":
    main()