def dpMC(cList, change, minCoins):
    for cents in range (1,change+1):
        coinCount = cents
        for j in [c for c in cList if c <= cents]:
            if minCoins[cents - j] + 1< coinCount:
                coinCount = minCoins[cents-j] + 1
        minCoins[cents] = coinCount

    return minCoins[change]

print(dpMC([1,5,10,21,25],63,[0]*64))
