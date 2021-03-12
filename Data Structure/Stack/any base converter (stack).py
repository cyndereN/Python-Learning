from pythonds.basic.stack import Stack

def divideby2(decNumber,base):
    r=Stack()
    digits="0123456789ABCDEF"
    while decNumber > 0:
        rem=decNumber % base
        r.push(rem)
        decNumber=decNumber // base

    string = ''
    while not r.isEmpty():
        string += digits[r.pop()]
    return string

print (divideby2(8,8))
