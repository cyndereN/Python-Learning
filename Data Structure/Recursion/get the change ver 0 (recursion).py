
def recMC(cList,change,lencList):
    if change%cList[lencList] == 0:
        return change//cList[lencList]
        
    else:
        c = change//cList[lencList]
        change = change%cList[lencList]
        cList.pop()
        lencList = len(cList) - 1
        return recMC(cList,change,lencList) + c
print(recMC([1,5,10,25],63,3))
