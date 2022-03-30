'''
Given an encoded string, return its decoded string.

The encoding rule is: k[encoded_string], where the encoded_string inside the square brackets is being repeated exactly k times. Note that k is guaranteed to be a positive integer.

You may assume that the input string is always valid; there are no extra white spaces, square brackets are well-formed, etc.

Furthermore, you may assume that the original data does not contain any digits and that digits are only for those repeat numbers, k. For example, there will not be input like 3a or 2[4].

Example 1:

Input: s = "3[a]2[bc]"
Output: "aaabcbc"

Example 2:

Input: s = "3[a2[c]]"
Output: "accaccacc"

Example 3:

Input: s = "2[abc]3[cd]ef"
Output: "abcabccdcdcdef"
'''

class Solution:
    def decodeString(self, s: str) -> str:
        
		# record of tuple ( previous token, repeat times of current token)
        stack = []
        
        cur_token, cur_number =  '', 0
        
        for char in s:
            
            if char == '[':
                # meet start symbol '['
                # save current token and current number into stack
                stack.append( (cur_token, cur_number) )
                
                # clear cur_token for new symbol in [ ]
                cur_token = ''
                
                # clear cur_number for new number in [ ]
                cur_number = 0
                
            elif char == ']':
                # meet ending symbol ']'
                # pop previous token and repeat times of current token from stack
                prev_token, repeat_times = stack.pop()
                
                # update current token with specified repeat times
                cur_token = prev_token + cur_token * repeat_times
                
            elif char.isdigit():
            
                # update current number
                cur_number = cur_number*10 + int(char)
            
            else:
                
                # update current token
                cur_token += char
                
                
        return cur_token
    
    
#####################################################################

class Solution:
    def decodeString(self, s: str) -> str: 
        exp = ""
        for i,a in enumerate(s):
            if a== '[':
                exp += '*('
            elif a == ']':
                exp += ')'
                if i != len(s)-1 and s[i+1] != ']':
                    exp += '+'       
            elif a.isdigit():
                exp += a 
            else:  #a.isalpha()
                exp += f"'{a}'"      
                if i<len(s)-1 and s[i+1] not in '[]':
                    exp += '+'

        return eval(exp)