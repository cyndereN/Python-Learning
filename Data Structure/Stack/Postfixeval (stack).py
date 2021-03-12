'''后缀运算式求值'''

class Stack:
    def __init__(self):
        self.items = []
    def push(self,item):
        self.items.append(item)
    def pop(self):
        return self.items.pop()
    def isEmpty(self):
        return (self.items ==[])
    def __str__(self):
        return str(self.items)

def postfixEval(postfixExpres):
         operandStack = Stack()
         tokenlist = postfixExpres.split()

         for token in tokenlist:
           if token in "0123456789":
             operandStack.push(int(token))
           else:
             operand2 = operandStack.pop
             operand1 = operandStack.pop
             result = doMath(token,operand1,operand2)
             operandStack.push(result)
         return operandStack.pop

def doMath(op,op1,op2):
       if op == "*":
        return op1*op2
       elif op == "/":
        return op1/op2
       elif op =="+":
        return op1 + op2
       elif op == "-":
        return op1 - op2

print(postfixEval('12+')) 
