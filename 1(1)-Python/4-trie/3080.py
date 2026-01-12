from lib import Trie
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