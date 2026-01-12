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

# Maximum rank of candies (1 to 1,000,000)
# Set slightly larger than 1,000,000 to prevent IndexError
MAX_RANK = 1_000_005


def main() -> None:
    # Read all input at once for performance
    input_data = sys.stdin.read().split()

    if not input_data:
        return

    iterator = iter(input_data)

    try:
        n_str = next(iterator, None)
        if n_str is None:
            return
        n = int(n_str)

        # External array to track the number of candies per flavor
        # Needed because our update() replaces the value, not adds to it
        candies = [0] * MAX_RANK

        # Initialize the Segment Tree
        seg = CntSegmentTree(0, MAX_RANK, candies)

        for _ in range(n):
            query_type = int(next(iterator))

            if query_type == 1:
                # Query 1: Pop the k-th rank candy
                rank = int(next(iterator))
                
                # Find the flavor index corresponding to the rank
                flavor_idx = seg.find_kth(rank)
                print(flavor_idx)

                # Decrement count and update tree
                candies[flavor_idx] -= 1
                seg.update(flavor_idx, candies[flavor_idx])

            else:
                # Query 2: Update candy count (add or remove)
                flavor_idx = int(next(iterator))
                count = int(next(iterator))

                # Update count and refresh tree
                candies[flavor_idx] += count
                seg.update(flavor_idx, candies[flavor_idx])

    except StopIteration:
        pass


if __name__ == "__main__":
    main()