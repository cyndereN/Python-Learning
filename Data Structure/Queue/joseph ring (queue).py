from pythonds.basic.queue import Queue
def joseph(namelist,num):
    simqueue=Queue()
    for name in namelist:
        simqueue.enqueue(name)

    while simqueue.size()>1:
        for i in range(num):
            simqueue.enqueue(simqueue.dequeue())
        simqueue.dequeue()
    return simqueue.dequeue()

list = ["Bill","David","Susan","Jane","Kent","Brad"]
print(joseph(list,5))
