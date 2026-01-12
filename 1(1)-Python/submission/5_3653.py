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


def main() -> None:
    """
    Main execution function for the Movie Collection problem.

    Reads input from stdin, processes multiple test cases, and prints
    the number of movies stacked above the selected movie for each query.
    """
    # Read all input at once for performance optimization
    input_data = sys.stdin.read().split()

    if not input_data:
        return

    iterator = iter(input_data)

    try:
        # Parse the number of test cases
        test_case_str = next(iterator, None)
        if test_case_str is None:
            return
        num_test_cases = int(test_case_str)

        while num_test_cases > 0:
            num_test_cases -= 1

            n_str = next(iterator, None)
            m_str = next(iterator, None)

            if n_str is None or m_str is None:
                break

            n, m = int(n_str), int(m_str)

            # Initialize the segment tree data array.
            # The first 'm' slots are empty buffers (0) for moved movies.
            # The next 'n' slots represent the initial movie positions (1).
            tree_data = [0] * m + [1] * n

            # Map movie ID to its current index in the segment tree.
            # Movie IDs are 1-based, so we prepend a dummy 0.
            # Initially, movie 'i' is at index 'm + i - 1' (0-based index).
            movie_indices = [0] + [i + m - 1 for i in range(1, n + 1)]

            # Initialize Segment Tree with the combined size (buffer + movies)
            segment_tree = CntSegmentTree(0, n + m, tree_data)

            for i in range(m):
                movie_id = int(next(iterator))

                # 1. Get the current position of the selected movie
                current_pos = movie_indices[movie_id]

                # 2. Query the sum from index 0 to current_pos
                # This sum represents the number of movies above the selected one
                print(segment_tree.query(0, current_pos), end=" ")

                # 3. Remove the movie from its current position (set to 0)
                segment_tree.update(current_pos, 0)

                # 4. Move the movie to the top (new position in the buffer)
                # The buffer is filled from right (m-1) to left (0)
                new_pos = m - 1 - i
                movie_indices[movie_id] = new_pos

                # 5. Mark the new position as occupied (set to 1)
                segment_tree.update(new_pos, 1)

            print()

    except StopIteration:
        pass


if __name__ == "__main__":
    main()