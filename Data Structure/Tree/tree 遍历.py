#前序
def preorder(tree):
    if tree:
        print(tree.getRootVal())
        preorder(tree.getLeftChild())
        preorder(tree.getRightChild())

#后序
def postorder(tree):
    if tree !=  None:
        postorder(tree.getLeftChild())
        postorder(tree.getRightChild())
        print(tree.getRootVal())

#中序
def inorder(tree):
        if tree !=  None:
            inorder(tree.getLeftChild())
            print(tree.getRootVal())
            inorder(tree.getRightChild())
        

