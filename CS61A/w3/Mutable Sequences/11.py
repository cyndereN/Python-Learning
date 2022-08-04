# Mutation

def f(s=[]):
    s.append(5)
    return len(s)

f() #1
f() #2
f() #3