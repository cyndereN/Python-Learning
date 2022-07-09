def trace1(fn):
    """
    fn - a function of 1 argument
    """
    
    def traced(x):
        print('Calling', fn, 'on argument', x)
        return fn(x)
    
    return traced

@trace1
def square(x):
    return x*x

# equals to square = trace1(square)

@trace1  # function decorator
def sum_squares_up_to(n):
    k = 1
    total = 0
    while k<=n:
        total, k = total + square(k), k+1
    return total