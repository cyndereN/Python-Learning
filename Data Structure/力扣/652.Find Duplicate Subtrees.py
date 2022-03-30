'''
Given the root of a binary tree, return all duplicate subtrees.

For each kind of duplicate subtrees, you only need to return the root node of any one of them.

Two trees are duplicate if they have the same structure with the same node values.


Example 1:
Input: root = [1,2,3,4,null,2,4,null,null,4]
Output: [[2,4],[4]]
'''

class Solution:
    def findDuplicateSubtrees(self, root: Optional[TreeNode]) -> List[Optional[TreeNode]]:
        self.ans = []
        c = collections.Counter()
        
        def _fds(root):
            if not root: return 'null'
            left = _fds(root.left)
            right = _fds(root.right)
            subtree = left+' '+right+' '+str(root.val)
            c[subtree] += 1
            if c[subtree] == 2:
                self.ans.append(root)
            return subtree
        
        _fds(root)
        
        return self.ans