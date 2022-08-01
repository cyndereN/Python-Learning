def prime_helper(n, i=2):
    if (n <= 2):
        return True if(n == 2) else False
    elif (n % i == 0):
        return False
    else: 
        if (i * i > n):
            return True
 
    # Check for next divisor
    return prime_helper(n, i+1)