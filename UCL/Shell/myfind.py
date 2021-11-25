import os
dirpath = input('请输入你要查找文件的开始目录:')
target = input('请输入你要查找的文件名:')
#dirpath = r'C:\Users\Administrator\Desktop'
#target = '1.txt'
#接收用户输出的目录路径
if dirpath == '':
    dirpath = os.getcwd()
    #如果用户没有输出，那么默认等于当前的脚本工作路径
    print('你当前要查找文件的开始目录为：%s' % dirpath)
 
def myfind(dirpath,target,level=0):
    level += 2
    for name in os.listdir(dirpath):
        #print('-' * level + '|' + name)
        #判断name是文件还是目录
        file_name = dirpath + '//' + name
        #print(file_name)
        #绝对路径,file_name
        if os.path.isfile(file_name):
            if target == name:
                print("查找到了:%s" % file_name)#打印绝对路径
                break#跳出查找循环
        if os.path.isdir(file_name):
            myfind(file_name,target,level)#找到是一个目录，那么继续进入查找
    return#终止函数
myfind(dirpath,target)