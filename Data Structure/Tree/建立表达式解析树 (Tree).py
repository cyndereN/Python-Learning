def buildParseTree(fpexp):
    fplist = fpexp.split()
    pStack = Stack()
    eTree = BinaryTree("")
    pStack.push(eTree) #入栈下降
    currentTree = eTree
    for i in fplist:
        if i =='(':
            currentTree.insertLeft('')
            pStack.push(curretTree) #入栈下降
            currentTree = currentTree.getLeftChild()
        elif i not in ['+','-','*','/']:
            currentTreesetRootVal(int(i))
            parent = pStack.pop()
            currentTree = parent #出栈上升
        elif i in ['+','-','*','/']:
            currentTree.setRootVal(i)
            currentTree.insertRight('')
            pStack.push(currentTree)
            currentTree = currentTree.getRightChild()
        elif i == ')':
            currentTree = pStack.pop()#出栈上升
        else:
            raise ValueError
    return eTree
