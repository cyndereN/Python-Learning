#coding=utf-8
# 本题为考试单行多行输入输出规范示例，无需提交，不计分。

# 输入包括两个正整数a,b(1 <= a, b <= 1000)。
# 输出a+b的结果
import sys 
for line in sys.stdin:
    a = line.split()
    print(int(a[0]) + int(a[1]))
    
# 单行+多行输入输出
# 读取第一行的n
n = int(sys.stdin.readline().strip())
ans = 0
for i in range(n):
    # 读取每一行
    line = sys.stdin.readline().strip()
    # 把每一行的数字分隔后转化成int列表
    values = list(map(int, line.split()))
    for v in values:
        ans += v
print(ans)


# 输入第一行包括一个数据组数t(1 <= t <= 100)
# 接下来每行包括两个正整数a,b(1 <= a, b <= 1000)
import sys
# 读取第一行的n
n = int(sys.stdin.readline().strip())
ans = 0
for i in range(n):
    line = sys.stdin.readline().strip()
    a = line.split()
    print(int(a[0]) + int(a[1]))
        
# 输入包括两个正整数a,b(1 <= a, b <= 10^9)
# 输入数据有多组, 如果输入为0 0则结束输入
import sys 
for line in sys.stdin:
    a, b = list(map(int,line.split(' ')))
    if a == 0 and b == 0:
        break
    else:
        print(a+b)


# 输入数据包括多组。
# 每组数据一行,每行的第一个整数为整数的个数n(1 <= n <= 100), n为0的时候结束输入。
# 接下来n个正整数,即需要求和的每个正整数。
import sys 
for line in sys.stdin:
    values = list(map(int, line.split()))
    if values[0] == 0:
        break
    else:
        print(sum(values[1:]))


# 输入的第一行包括一个正整数t(1 <= t <= 100), 表示数据组数。
# 接下来t行, 每行一组数据。
# 每行的第一个整数为整数的个数n(1 <= n <= 100)。
# 接下来n个正整数, 即需要求和的每个正整数。
import sys
n = int(sys.stdin.readline().strip())
ans = 0
for i in range(n):
    # 读取每一行
    line = sys.stdin.readline().strip()
    # 把每一行的数字分隔后转化成int列表
    values = list(map(int, line.split()))
    print(sum(values[1:]))
        
        
# 输入数据有多组, 每行表示一组输入数据。
# 每行的第一个整数为整数的个数n(1 <= n <= 100)。
# 接下来n个正整数, 即需要求和的每个正整数。      
import sys 
for line in sys.stdin:
    values = list(map(int, line.split()))
    print(sum(values[1:]))
    
# 输入数据有多组, 每行表示一组输入数据。
# 每行不定有n个整数，空格隔开。(1 <= n <= 100)。
import sys 
for line in sys.stdin:
    values = list(map(int, line.split()))
    print(sum(values[:]))   # print(sum(values))
    
# 输入有两行，第一行n
# 第二行是n个字符串，字符串之间用空格隔开
# 输出一行排序后的字符串，空格隔开，无结尾空格
import sys 
n = int(sys.stdin.readline().strip())
strlist = sys.stdin.readline().strip().split(' ')
strlist.sort()
strlist = " ".join(strlist)
print(strlist)

# 多个测试用例，每个测试用例一行。
# 每行通过空格隔开，有n个字符，n＜100
# 对于每组测试用例，输出一行排序过的字符串，每个字符串通过空格,逗号隔开
import sys 
for line in sys.stdin:
    strlist = line.strip().split(',')
    strlist.sort()
    strlist = ",".join(strlist)
    print(strlist)