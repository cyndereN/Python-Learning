import os
import shlex

command_to_run = shlex.split(input('输入想要执行的程序：'))
input('按下回车键后会执行os.fork')
child_pid = os.fork()

if child_pid == 0:  # 如果返回值是0，代表此时在子进程中
    print('[子进程] 这个print在子进程里头')
    print(f'[子进程] 这是想要运行的程序：{command_to_run}')
    os.execvp(command_to_run[0], command_to_run)
    print('[子进程] 我们看不到这个print')
    # 我们看不到这个print，因为执行os.execvp时，
    # 当前进程的代码和数据，会被替换为想要执行的程序的代码和数据
else:
    print('[父进程] 这个print在父进程里')
    print('[父进程] 即将进入while循环')
    while True:
        pass

# 输入想要执行的程序：echo "我是一个程序，名字叫echo"
# 按下回车键后会执行os.fork
# [父进程] 这个print在父进程里
# [子进程] 这个print在子进程里头
# [父进程] 即将进入while循环
# [子进程] 这是想要运行的程序：['echo', '我是一个程序，名字叫echo']
# 我是一个程序，名字叫echo


'''----------------------------------------------------------------------'''

import os
import shlex

command_to_run = shlex.split(input('输入想要执行的程序：'))
input('按下回车键后会执行os.fork')
child_pid = os.fork()

if child_pid == 0:  # 如果返回值是0，代表此时在子进程中
    print('[子进程] 这个print在子进程里头')
    print(f'[子进程] 这是想要运行的程序：{command_to_run}')
    os.execvp(command_to_run[0], command_to_run)
    print('[子进程] 我们看不到这个print')
    # 我们看不到这个print，因为执行os.execvp时，
    # 当前进程的代码和数据，会被替换为想要执行的程序的代码和数据
else:
    print('[父进程] 这个print在父进程里')
    print('[父进程] 即将调用os.waitpid(child_pid, 0)')
    os.waitpid(child_pid, 0)  # 调用了os.waitpid
    print('[父进程] 子进程退出了，现在轮到我退出了')


# 输入想要执行的程序：python3
# 按下回车键后会执行os.fork
# [父进程] 这个print在父进程里
# [父进程] 即将调用os.waitpid(child_pid, 0)
# [子进程] 这个print在子进程里头
# [子进程] 这是想要运行的程序：['python3']
# Python 3.7.3 (v3.7.3:ef4ec6ed12, Mar 25 2019, 16:52:21)
# [Clang 6.0 (clang-600.0.57)] on darwin
# Type "help", "copyright", "credits" or "license" for more information.
# >>> quit()
# [父进程] 子进程退出了，现在轮到我退出了


'''-----------------------------------------------------------------------'''
import os
import shlex

if __name__ == "__main__":
    while True:
        command_to_run = shlex.split(input('输入想要执行的程序：'))
        if command_to_run[0] == 'exit':
            exit(0)

        child_pid = os.fork()
        if child_pid == 0:
            os.execvp(command_to_run[0], command_to_run)
        else:
            os.waitpid(child_pid, 0)  # 调用了os.waitpid

