# (BOJ) Skeleton Code Provided by YBIGTA

from __future__ import annotations
from typing import TypeVar, Generic, Callable


"""
TODO:
- SegmentTree 구현하기
"""


T = TypeVar("T")


class SegmentTree(Generic[T]):
    """
    A generic, iterative Segment Tree implementation.

    This class supports point updates and range queries for any associative
    operation (e.g., sum, min, max, gcd).
    """
    __slots__ = ('_size', '_identity', '_func', '_tree')

    def __init__(
        self,
        func: Callable[[T, T], T],
        identity: T,
        size: int,
        data: list[T]
    ) -> None:
        self._size = size
        self._identity = identity
        self._func = func
        self._tree: list[T] = [identity] * 2 * size

        # Copy data to leaves (indices size to 2*size - 1)
        self._tree[size : size + len(data)] = data

        # Build the tree by calculating parents in reverse order
        for i in range(size - 1, 0, -1):
            self._tree[i] = self._func(
                self._tree[i << 1], self._tree[i << 1 | 1]
            )

    def update(self, idx: int, val: T) -> None:
        """Updates the value at index `idx` and refreshes the tree."""
        tree = self._tree
        func = self._func

        idx += self._size
        tree[idx] = val

        # Bubble up the changes to the root
        while idx > 1:
            idx >>= 1
            tree[idx] = func(
                tree[idx << 1], tree[idx << 1 | 1]
            )

    def query(self, left: int, right: int) -> T:
        """
        Queries the range [left, right) and returns the aggregated result.

        Args:
            left (int): The starting index (inclusive).
            right (int): The ending index (exclusive).
        """
        tree = self._tree
        func = self._func
        left += self._size
        right += self._size
        lres: T = self._identity
        rres: T = self._identity

        while left < right:
            # If left is odd, it's a right child; include it and move inward
            if left & 1:
                lres = func(lres, tree[left])
                left += 1

            # If right is odd, it's a right child; decrement to get left child
            if right & 1:
                right -= 1
                rres = func(tree[right], rres)

            # Move up to parents
            left >>= 1
            right >>= 1

        return func(lres, rres)
    
class CntSegmentTree(SegmentTree[int]):
    """
    A specialized Segment Tree for integer counting and summation.

    This class extends SegmentTree to support finding the k-th element
    based on the accumulated counts in the tree nodes.
    """

    def __init__(self, identity: int, size: int, data: list[int]) -> None:
        # We should Top-Down -> need to be modified by 2^n
        modified_size = 1
        while modified_size < size:
            modified_size <<= 1

        # Use a lambda for integer addition
        super().__init__(lambda x, y: x + y, identity, modified_size, data)

    def find_kth(self, k: int) -> int:
        """
        Finds the original index of the k-th item (1-based rank).
        """
        idx = 1
        tree = self._tree  # Local variable caching for performance

        # Traverse down to the leaf node
        while idx < self._size:
            left_child = 2 * idx
            cnt = tree[left_child]

            if k <= cnt:
                # The target is in the left subtree
                idx = left_child
            else:
                # The target is in the right subtree; skip the left part
                idx = 2 * idx + 1
                k -= cnt

        return idx - self._size


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