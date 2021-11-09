from lark import Lark
from lark import Transformer

json_parser = Lark(r"""
    value: dict
         | list
         | ESCAPED_STRING
         | SIGNED_NUMBER
         | "true" | "false" | "null"

    list : "[" [value ("," value)*] "]"

    dict : "{" [pair ("," pair)*] "}"
    pair : ESCAPED_STRING ":" value

    %import common.ESCAPED_STRING
    %import common.SIGNED_NUMBER
    %import common.WS
    %ignore WS

    """, start='value')

text = '{"key": ["item0", "item1", 3.14, true]}'

print( json_parser.parse(text).pretty() )

# value
#   dict
#     pair
#       "key"
#       value
#         list
#           value "item0"
#           value "item1"
#           value 3.14
#           value 


json_parser = Lark(r"""
    ?value: dict
          | list
          | string
          | SIGNED_NUMBER      -> number
          | "true"             -> true
          | "false"            -> false
          | "null"             -> null

    list : "[" [value ("," value)*] "]"

    dict : "{" [pair ("," pair)*] "}"
    pair : string ":" value

    string : ESCAPED_STRING

    %import common.ESCAPED_STRING
    %import common.SIGNED_NUMBER
    %import common.WS
    %ignore WS

    """, start='value')

parse_tree = json_parser.parse(text)
print( parse_tree.pretty() )

# dict
#   pair
#     string      "key"
#     list
#       string    "item0"
#       string    "item1"
#       number    3.14
#       true

class TreeToJson(Transformer):
    def list(self, items):
        return list(items)
    def pair(self, key_value):
        k, v = key_value
        return k, v
    def dict(self, items):
        return dict(items)

print(TreeToJson().transform(parse_tree))

#{Tree('string', [Token('ESCAPED_STRING', '"key"')]): [Tree('string', [Token('ESCAPED_STRING', '"item0"')]), Tree('string', [Token('ESCAPED_STRING', '"item1"')]), Tree('number', [Token('SIGNED_NUMBER', '3.14')]), Tree('true', [])]}

class TreeToJson(Transformer):
    def string(self, s):
        (s,) = s
        return s[1:-1]
    def number(self, n):
        (n,) = n
        return float(n)

    list = list
    pair = tuple
    dict = dict

    null = lambda self, _: None
    true = lambda self, _: True
    false = lambda self, _: False

print(TreeToJson().transform(parse_tree))
#{'key': ['item0', 'item1', 3.14, True]}

json_grammar = r"""
    ?start: value

    ?value: object
          | array
          | string
          | SIGNED_NUMBER      -> number
          | "true"             -> true
          | "false"            -> false
          | "null"             -> null

    array  : "[" [value ("," value)*] "]"
    object : "{" [pair ("," pair)*] "}"
    pair   : string ":" value

    string : ESCAPED_STRING

    %import common.ESCAPED_STRING
    %import common.SIGNED_NUMBER
    %import common.WS

    %ignore WS
"""

json_parser = Lark(json_grammar, parser='lalr',
                   # Using the basic lexer isn't required, and isn't usually recommended.
                   # But, it's good enough for JSON, and it's slightly faster.
                   lexer='standard',
                   # Disabling propagate_positions and placeholders slightly improves speed
                   propagate_positions=False,
                   maybe_placeholders=False,
                   # Using an internal transformer is faster and more memory efficient
                   transformer=TreeToJson())
parse = json_parser.parse