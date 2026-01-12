# (BOJ) Skeleton Code Provided by YBIGTA

import sys

"""
TODO:
- Trie.push 구현하기
- (필요할 경우) Trie에 추가 method 구현하기
"""

class Trie:
    # Use __slots__ to enforce structure, though we don't use node objects here.
    __slots__ = ('child', 'sibling', 'info')

    def __init__(self) -> None:
        # Instead of creating TrieNode objects, we use parallel lists.
        
        # child[u]: Index of the first child of node u (-1 if none)
        self.child: list[int] = [-1]
        
        # sibling[u]: Index of the next sibling of node u (-1 if none)
        self.sibling: list[int] = [-1]
        
        # info[u]: Packed integer storing (char_index << 1) | is_end
        # - Character code: info[u] >> 1
        # - Is End of Word: info[u] & 1
        self.info: list[int] = [0]

    def _new_node(self, char_code: int) -> int:
        """
        Create a new node by appending to arrays.
        """
        self.child.append(-1)
        self.sibling.append(-1)
        # Shift char_code by 1 to make room for the is_end bit
        self.info.append(char_code << 1)
        return len(self.child) - 1

    def _char_to_index(self, char: str) -> int:
        """
        Convert char to 0-25 index (Handles both upper/lower case).
        """
        if 'a' <= char <= 'z':
            return ord(char) - ord('a')
        else:
            return ord(char) - ord('A')

    def push(self, seq: str) -> None:
        """
        seq: T의 열 (list[int]일 수도 있고 str일 수도 있고 등등...)

        action: trie에 seq을 저장하기
        """
        curr = 0  # Start at root (index 0)
        
        for char in seq:
            code = self._char_to_index(char)
            
            # 1. Search for the child in the sibling linked list
            prev = -1
            curr_child = self.child[curr]
            found_idx = -1
            
            while curr_child != -1:
                # Extract char code using bitwise shift
                if (self.info[curr_child] >> 1) == code:
                    found_idx = curr_child
                    break
                prev = curr_child
                curr_child = self.sibling[curr_child]
            
            if found_idx != -1:
                # Path exists
                curr = found_idx
            else:
                # Path does not exist: create new node
                new_idx = self._new_node(code)
                
                # Insert at the head of the linked list (O(1))
                self.sibling[new_idx] = self.child[curr]
                self.child[curr] = new_idx
                
                curr = new_idx
        
        # Mark end of word (Set the last bit to 1)
        self.info[curr] |= 1


import sys


"""
TODO:
- 일단 lib.py의 Trie Class부터 구현하기
- main 구현하기

힌트: 한 글자짜리 자료에도 그냥 str을 쓰기에는 메모리가 아깝다...
"""

MOD = 1_000_000_007
MAX_N = 3000

# Pre-compute factorials
fact = [1] * (MAX_N + 1)
for i in range(2, MAX_N + 1):
    fact[i] = (fact[i - 1] * i) % MOD

def main() -> None:
    input_data = sys.stdin.read().split()
    if not input_data: return
    
    iterator = iter(input_data)
    
    try:
        if not input_data: return
        N = int(next(iterator))
        
        trie = Trie()
        
        for _ in range(N):
            trie.push(next(iterator))
            
        ans = 1
        
        # Iterate over all nodes created in the Trie
        # total_nodes is the length of the arrays
        total_nodes = len(trie.child)
        
        for u in range(total_nodes):
            cnt = 0
            
            # Count the number of children for node u
            # Traverse the sibling linked list
            curr_child = trie.child[u]
            while curr_child != -1:
                cnt += 1
                curr_child = trie.sibling[curr_child]
            
            # Check if node u marks the end of a word using bitwise AND
            if trie.info[u] & 1:
                cnt += 1
                
            # If there are items to arrange, multiply by factorial
            if cnt > 0:
                ans = (ans * fact[cnt]) % MOD
            
        print(ans)
            
    except StopIteration:
        pass

if __name__ == "__main__":
    main()