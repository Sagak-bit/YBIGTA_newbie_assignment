from lib import Trie
import sys


"""
TODO:
- 일단 Trie부터 구현하기
- count 구현하기
- main 구현하기
"""

def get_child_count(trie: Trie, u: int) -> int:
    """
    Helper to count children by traversing the sibling array.
    """
    cnt = 0
    curr = trie.child[u]
    while curr != -1:
        cnt += 1
        curr = trie.sibling[curr]
    return cnt

def count(trie: Trie, query_seq: str) -> int:
    """
    trie - 이름 그대로 trie
    query_seq - 단어 ("hello", "goodbye", "structures" 등)

    returns: query_seq의 단어를 입력하기 위해 버튼을 눌러야 하는 횟수
    """
    pointer = 0
    cnt = 0

    for element in query_seq:
        char_code = ord(element) - ord('a')
        
        # 1. Check for branching
        child_count = get_child_count(trie, pointer)
        # Check is_end using bitwise AND
        is_end = (trie.info[pointer] & 1)

        # Increment keystrokes if ambiguity exists or previous word ended here
        if child_count > 1 or is_end:
            cnt += 1

        # 2. Move to child node
        curr = trie.child[pointer]
        while curr != -1:
            # Check character code using bitwise shift
            if (trie.info[curr] >> 1) == char_code:
                pointer = curr
                break
            curr = trie.sibling[curr]

    # Handle the first character rule:
    # If root has 1 child, the loop doesn't count the first key.
    # But the 1st key is mandatory.
    root_child_count = get_child_count(trie, 0)
    return cnt + int(root_child_count == 1)


def main() -> None:
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        while True:
            try:
                N = int(next(iterator))
            except StopIteration:
                break

            words = []
            
            # Reset Trie for each test case
            trie = Trie()
            
            for _ in range(N):
                word = next(iterator)
                words.append(word)
                trie.push(word)
            
            total_keystrokes = 0
            for word in words:
                total_keystrokes += count(trie, word)
            
            print(f"{total_keystrokes / N:.2f}")
            
    except StopIteration:
        pass

if __name__ == "__main__":
    main()