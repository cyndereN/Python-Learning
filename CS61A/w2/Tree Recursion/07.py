# Tree recursion

def fib(n):
    """Compute the nth Fibonacci number.

    >>> fib(8)
    21
    """
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-2) + fib(n-1)


def paths(m, n):
    """
    Return the number of paths from one corner of an M by N grid to the opposite corner.
    
    >>> paths(2,2)
    2
    >>> paths(117, 1)
    1
    """
    if m==1 or n==1:
        return 1
    return paths(m-1,n) + paths(m,n-1)

#Count Partitions
def count_partitions(n, m):
    """Count the partitions of n using parts up to size m.

    >>> count_partitions(6, 4)
    9
    >>> count_partitions(10, 10)
    42
    """
    if n == 0:
        return 1
    elif n < 0:
        return 0
    elif m == 0:
        return 0
    else:
        with_m = count_partitions(n-m, m)
        without_m = count_partitions(n, m-1)
        return with_m + without_m

#Binary Print

def all_nums(k):
    def h(k, prefix):
        if k == 0:
            print(prefix)
            return
        h(k - 1, prefix * 10)
        h(k - 1, prefix * 10 + 1)
    h(k, 0)

# Remove digits
def remove(n, digit):
    """
    Return all digits of non-negative N that are not DIGIT
    
    >>> remove(213,3)
    21
    """
    
    kept, digits = 0, 0
    while n>0:
        n, last = n//10, n%10
        if last!=digit:
            kept = kept + last*10**digits
            digits = digit+1
    return kept