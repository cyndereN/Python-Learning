import time

aList = []
count = 0

while count<10000000:
    aList.append(count)
    count += 1

starttime = time.time()
count = 0
while count<10000000:
    aList.pop(len(aList)//2) #from middle
    if count%100 == 0:
        now = time.time()
        print(now - starttime, count)
    count += 1