def recMC(cList,change):
    minCoins = change
    if change in cList:
        return 1
    else:
        for i in [c for c in cList if c <= change]:
            numCoins = 1 + recMC(cList, change-i)
            if numCoins < minCoins:
                minCoins = numCoins
    return minCoins


print(recMC([1,5,10,25],63))
