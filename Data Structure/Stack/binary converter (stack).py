from pythonds.basic.stack import Stack

def divideby2(decNumber):
    r=Stack()

    while decNumber > 0:
        rem=decNumber % 2
        r.push(rem)
        decNumber=decNumber//2

    binString = ''
    while not r.isEmpty():
        binString += str(r.pop())
    return binString

print (divideby2(8))
