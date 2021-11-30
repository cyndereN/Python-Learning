import math

def prime_factors(n):
    '''Return the prime factors of a given number.'''
    result = []
    divisor = 2
    while n>1 :
        if n%divisor == 0:
            result.append(divisor)
            n = int(n/divisor)
        else:
            divisor = divisor + 1
            if divisor > math.sqrt(n):
                divisor = n
        return result
        