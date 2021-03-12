from pythonds.basic.stack import Stack


s=Stack()

print(s.isEmpty())
s.push(4)
s.push('dog')
print(s.peek())
s.push(True)
print(s.size())
print(s.isEmpty())
s.push(8.4)
print(s.pop())
print(s.pop())
print(s.size())
s.pop()
s.peek()
s.size()
'''
class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        # 判断是否为空
        return self.items == []

    def push(self, item):
        # 压入一个元素，无返回值
        self.items.append(item)

    def pop(self):
        # 弹出一个元素
        return self.items.pop()

    def peek(self):
        # 返回top元素，不改变原Stack
        return self.items[len(self.items) - 1]

    def size(self):
        # 返回Stack的大小
        return len(self.items)
'''
