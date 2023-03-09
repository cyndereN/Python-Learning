class BinHeap: #最小堆
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


    
    # 因为是最小堆，由大到小排序。不断重建小顶堆O(nlogn)
    def heapSortReturnNewArr(self):
        # 存到一个新数组中
        arr = self.heapList[1:]
        for j in range(self.currentSize-1, 0, -1):
            arr[0], arr[j] = arr[j], arr[0]
            
            # 初始位置
            i = 0
            # 左节点的位置
            p = 2 * i + 1 
            while (p <= j-1):
            # 如果右节点存在
                if p + 1 <= j-1:
                    # 选出左右节点中 较小的与父节点比较
                    p = p if arr[p] < arr[p + 1] else p + 1
                # 当父节点较大时 继续进行交换
                if arr[i] > arr[p]:
                    arr[i], arr[p] = arr[p], arr[i]
                else:  # 否则 退出循环
                    break
                i = p
                p = 2 * i + 1

        print(arr)
        print(self.heapList)
        
    # 原地排序，不需要额外的空间。O(nlogn)
    # 堆排序本质还是选择排序。适合排序序列个数多的情况(建堆所需比较次数较多)
    def heapSort(self):
        for j in range(self.currentSize , 1, -1):
            self.heapList[1], self.heapList[j] = self.heapList[j], self.heapList[1]
            self.heapify(1, j-1)

        print(self.heapList)
        

    def heapify(self, i, heapSize):
         # 左节点的位置
        p = 2 * i 
        while (p <= heapSize):
            # 如果右节点存在
            if p + 1 <= heapSize:
                # 选出左右节点中 较小的与父节点比较
                p = p if self.heapList[p] < self.heapList[p + 1] else p + 1
            # 当父节点较大时 继续进行交换
            if self.heapList[i] > self.heapList[p]:
                self.heapList[i], self.heapList[p] = self.heapList[p], self.heapList[i]
            else:  # 否则 退出循环
                break
            i = p
            p = 2 * i 

            
lis = BinHeap()
lis.buildHeap([5, 9, 1, 6, 8, 14, 6, 49, 25, 4, 6, 3])
lis.heapSort()