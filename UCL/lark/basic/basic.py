from lark import Lark
from lark import Transformer

with open("Grammar.lark",encoding="utf-8") as grammar:
    LP = Lark(grammar.read(),start="script")

tree = LP.parse("rand -s3 a b c + say def | replace e E")
#print(tree.pretty())

# script
#   chunk
#     sentence
#       command
#         chars   rand
#       space
#       option
#         chars   s3
#       space
#       arg
#         chars   a
#       space
#       arg
#         chars   b
#       space
#       arg
#         chars   c
#   join
#     space
#     space
#   chunk
#     sentence
#       command
#         chars   say
#       space
#       arg
#         chars   def
#     pipe
#       space
#       space
#     sentence
#       command
#         chars   replace
#       space
#       arg
#         chars   e
#       space
#       arg
#         chars   E


class mytransformer(Transformer):
    def __init__(self): #Initialize variables to be used as appropriate
        self.var1 = None
        self.var2 = []

    def sentence(self,tree): #If you take the second argument, you can use a tree deeper than sentence!
        print("sentence") # example

    def command(self,tree):
        print("command")

    def option(self,tree):
        print("option")

tree = LP.parse("rand -s3 a b c + say def | replace e E")
print(mytransformer().transform(tree))