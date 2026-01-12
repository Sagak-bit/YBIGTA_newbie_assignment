from lib import CntSegmentTree
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