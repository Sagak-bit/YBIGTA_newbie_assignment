from lib import SegmentTree
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