# lib.py의 Matrix 클래스를 참조하지 않음
import sys


"""
TODO:
- fast_power 구현하기 
"""


def fast_power(base: int, exp: int, mod: int) -> int:
    """
    빠른 거듭제곱 알고리즘 구현
    분할 정복을 이용, 시간복잡도 고민!
    """
    result = 1
    # Ensure base is within the modulus range initially
    base %= mod
    
    while exp > 0:
        # Check if the least significant bit (LSB) is 1
        # (i.e., current exp is odd)
        if exp & 1:
            result = (result * base) % mod

        # Square the base for the next bit position
        base = (base * base) % mod
        
        # Right shift the exponent by 1 (equivalent to exp // 2)
        exp >>= 1
        
    return result

def main() -> None:
    A: int
    B: int
    C: int
    A, B, C = map(int, input().split()) # 입력 고정
    
    result: int = fast_power(A, B, C) # 출력 형식
    print(result) 

if __name__ == "__main__":
    main()
