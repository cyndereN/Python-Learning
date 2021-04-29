class BinHeap:
    def __init__(self):
        self.heapList = [0] #0占位 根节点从1开始
        self.currentSize = 0

    def percUp(self,i):
        while i//2 >0:
            if self.heapList[i] < self.heapList[i//2]:
                tmp = self.heapList[i//2] #与父节点交换
                self.heapList[i//2]
                self.heaplist[i//2]=self.heapList[i]
                self.heapList[i]=tmp
            i=i//2 #沿路径向上
    def insert(self,k):
        self.heapList.append(k)#添加到末尾
        self.currentSize = self.currentSize + 1
        self.percUp(self.currentSize) #新key上浮

    def minChild(self,i):
        if i*2+1>self.currentSize:
            return i*2
        else:
            if self.heapList[i*2] < self.heapList[i*2+1]:
                return i*2
            else:
                return i*2+1
    def percDown(self,i):
        while(i*2) <= self.currentSize:
            mc = self.minChild(i)
            if self.heapList[i] > self.heapList[mc]:
                tmp = self.heapList[i]
                self.heapList[i] = self.heapList[mc]
                self.heapList[mc] = tmp
            i = mc
    def delMin(self):
        retval = self.heapList[1]
        self.heapList[1] = self.heapList[self.currentSize]
        self.currentSize = self.currentSize - 1
        self.heapList.pop()
        self.percDown(1)
        return retval

    def buildHeap(self,alist):
        i = len(alist)//2
        self.currentSize = len(alist)
        self.heapList = [0] + alist[:]
        print(len(self.heapList),i)
        while (i>0):
            print(self.heapList,i)
            self.percDown(i)
            i=i-1
        print(self.heapList,i)
