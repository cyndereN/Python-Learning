def build_heap(arr, i): 
    # 当子节点大于父节点，交换
    while (arr[i] > arr[(i - 1) // 2] and i > 0):
        arr[i], arr[(i - 1) // 2] = arr[(i - 1) // 2], arr[i]
        # 继续向上交换
        i = (i - 1) // 2

def heapify(arr, i, heap_size):
    # 左节点的位置
    p = 2 * i + 1
    while (p <= heap_size):
        # 如果右节点存在
        if p + 1 <= heap_size:
            # 选出左右节点中 较大的与父节点比较
            p = p if arr[p] > arr[p + 1] else p + 1
        # 当父节点较小时 继续进行交换
        if arr[i] < arr[p]:
            arr[i], arr[p] = arr[p], arr[i]
        else:  # 否则 退出循环
            break
        i = p
        p = 2 * i + 1
    return arr

    
if __name__ == '__main__':
    arr = [3, 8, 5, 2, 9, 5]
    
    # 建立大顶堆, O(n)
    for i in range(len(arr)):
        build_heap(arr, i)

    # 不断调整堆顶元素 进行大顶堆重建，O(n*log(n))
    for j in range(len(arr) - 1, 0, -1):
        arr[0], arr[j] = arr[j], arr[0]
        heapify(arr, 0, j-1)
    
    # 整体时间复杂度: O(n) + O(n*log(n)) = O(n*log(n))
    print(arr)


# 那么有人会疑惑为什么不使用小堆排升序呢？
# 我们再想想：首先使用堆排序主要是用堆顶元素，如果使用小堆排升序，
# 此时堆顶的元素是最小的，当我们取出堆顶元素时，此时小根堆的性质就变了，
# 那么下次就找不到第二小的元素了，还要重新建堆。所以不能使用小堆排升序。

# 堆排序本质还是选择排序。适合排序序列个数多的情况(建堆所需比较次数较多)