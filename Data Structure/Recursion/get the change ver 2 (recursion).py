def recMC(cList,change,knowResults):
    minCoins = change
    if change in cList:
        knowResults[change] = 1
        return 1
    elif knowResults[change] > 0:
        return knowResults[change]
    else:
        for i in [c for c in cList if c <= change]:
            numCoins = 1 + recMC(cList, change-i,\
                                   knowResults)
            if numCoins < minCoins:
                minCoins = numCoins
                knowResults[change] = minCoins
    return minCoins


print(recMC([1,5,10,25],63,[0]*64))
