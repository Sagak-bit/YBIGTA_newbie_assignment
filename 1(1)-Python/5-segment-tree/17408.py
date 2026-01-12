from lib import SegmentTree
import sys


"""
TODO:
- 일단 SegmentTree부터 구현하기
- main 구현하기
"""


class Pair(tuple[int, int]):
    """
    힌트: 2243, 3653에서 int에 대한 세그먼트 트리를 만들었다면
    여기서는 Pair에 대한 세그먼트 트리를 만들 수 있을지도...?
    """
    def __new__(cls, a: int, b: int) -> 'Pair':
        return super().__new__(cls, (a, b))

    @staticmethod
    def default() -> 'Pair':
        """
        기본값
        이게 왜 필요할까...?
        """
        return Pair(0, 0)

    @staticmethod
    def f_conv(w: int) -> 'Pair':
        """
        원본 수열의 값을 대응되는 Pair 값으로 변환하는 연산
        이게 왜 필요할까...?
        """
        return Pair(w, 0)

    @staticmethod
    def f_merge(a: Pair, b: Pair) -> 'Pair':
        """
        두 Pair를 하나의 Pair로 합치는 연산
        이게 왜 필요할까...?
        """
        return Pair(*sorted([*a, *b], reverse=True)[:2])

    def sum(self) -> int:
        return self[0] + self[1]


def main() -> None:
    """
    Main execution function for Sequence and Queries 24.
    """
    input_data = sys.stdin.read().split()

    if not input_data:
        return

    iterator = iter(input_data)

    n_str = next(iterator, None)
    if n_str is None:
        return
    n = int(n_str)

    # Read initial numbers
    numbers: list[int] = []
    for _ in range(n):
        element = int(next(iterator))
        numbers.append(element)

    # Convert integers to Pair objects for the Segment Tree
    pair_data = [Pair.f_conv(x) for x in numbers]

    m_str = next(iterator, None)
    if m_str is None:
        return
    m = int(m_str)

    # Initialize SegmentTree with Pair merge function and identity value
    seg = SegmentTree(Pair.f_merge, Pair.default(), n, pair_data)

    for _ in range(m):
        query_type = int(next(iterator))

        if query_type == 1:
            # Update query: 1 i v
            # Change the value at index i to v
            idx = int(next(iterator))
            val = int(next(iterator))
            
            # Convert 1-based index to 0-based
            idx -= 1
            
            # Update local list (optional but good for consistency) and tree
            # Note: We must convert the integer 'val' to a 'Pair'
            new_pair = Pair.f_conv(val)
            seg.update(idx, new_pair)

        else:
            # Sum query: 2 l r
            # Print the sum of the two largest values in range [l, r]
            l = int(next(iterator))
            r = int(next(iterator))
            
            # Convert 1-based start index to 0-based
            # Range end 'r' is exclusive in 0-based indexing,
            # which matches the inclusive 1-based 'r'.
            l -= 1
            
            print(seg.query(l, r).sum())


if __name__ == "__main__":
    main()