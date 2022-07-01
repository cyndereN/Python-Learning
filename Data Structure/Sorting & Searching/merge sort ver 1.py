def mergeSort(alist):
    if len(alist)<=1:
        return alist

    middle = len(alist) // 2
    left = mergeSort(alist[:middle])
    right = mergeSort(alist[middle:])

    merged = []
    while left and right:
        if left[0] <= right[0]:
            merged.append(left.pop(0))
        else:
            merged.append(right.pop(0))

    merged.extend(right if right else left)
    return merged

alist = [1,2,3,4,5,8,7,6]
alist = mergeSort(alist)
print(alist)


'''分裂：O(logn)
   归并：O(n)
   总：O(nlogn)
   需要额外一倍储存空间'''
