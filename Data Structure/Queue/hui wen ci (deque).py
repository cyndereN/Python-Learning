from pythonds.basic.deque import Deque

def palchecker(aString):
    chardeque = Deque()

    for c in aString:
        chardeque.addRear(c)

    stillEqual = True

    while chardeque.size()>1 and stillEqual:
        first = chardeque.removeFront()
        last = chardeque.removeRear()
        if first != last:
            stillEqual = False
    return stillEqual

print(palchecker("radar"))
