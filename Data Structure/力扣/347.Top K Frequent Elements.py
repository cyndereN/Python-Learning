'''
Given an integer array nums and an integer k, return the k most frequent elements. You may return the answer in any order.


Example 1:

Input: nums = [1,1,1,2,2,3], k = 2
Output: [1,2]

Example 2:

Input: nums = [1], k = 1
Output: [1]
'''
class Solution(object):
    def topKFrequent(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: List[int]
        """
        bucket = [None] * (len(nums) + 1)
        for i in range(len(nums)+1):
            bucket[i] = []
        d = {}
        
        for i in nums:
            if i not in d:
                d[i] = 1
            else:
                d[i] += 1
        ans = []
        
        for i in d:
            bucket[d[i]].append(i)
        for i in range(len(bucket)-1,-1,-1):
            if len(bucket[i]) != 0:
                for eachbucketElement in bucket[i]:
                    ans.append(eachbucketElement)
        return ans[:k]
