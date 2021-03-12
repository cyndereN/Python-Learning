def toStr(n,base):
    cString="0123456789ABCDEF"
    if n < base:
        return cString[n]
    else:
        return  toStr(n//base,base) + cString[n%base]


print(toStr(1024,2))
