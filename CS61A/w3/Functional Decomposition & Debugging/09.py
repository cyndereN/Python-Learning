# Assertion

from pygame import init


def fact(x):
    ########
    assert isinstance(x, int)
    assert x >=0
    ########
    if x==0:
        return 1
    else:
        return x*fact(x-1)

def half_fact(x):
    return fact(x/2)

print(half_fact(5))


# Try Statement
def invert(x):
    y = 1/x
    print('Never printed if x is 0')
    return y

def invert_safe(x):
    try:
        return invert(x)
    except ZeroDivisionError as e:
        print('handled', e)
        return 0


# reduce

def reduce(f, s, initial):
    """
    Combine elements of s using f starting with initial  
    """
    for x in s:
        initial = f(initial, x)
    return initial

def reduce(f, s, initial):
    """
    Combine elements of s using f starting with initial  
    """
    if not s:
        return initial
    else:
        first, rest = s[0], s[1:]
        return reduce(f, rest, f(initial, first))