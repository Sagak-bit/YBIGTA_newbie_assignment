from __future__ import annotations
import copy


class Matrix:
    """
    A class to represent a matrix and perform matrix operations
    under a specific modulo.
    """
    MOD = 1000

    def __init__(self, matrix: list[list[int]]) -> None:
        """
        Initializes the Matrix object.

        Args:
            matrix (list[list[int]]): A 2D list representing the matrix data.
        """
        self.matrix = [[elem % self.MOD for elem in row] for row in matrix]

    @staticmethod
    def full(n: int, shape: tuple[int, int]) -> Matrix:
        """
        Creates a matrix of a given shape filled with the value n.

        Args:
            n (int): The value to fill the matrix with.
            shape (tuple[int, int]): A tuple (rows, columns).

        Returns:
            Matrix: A new Matrix object.
        """
        return Matrix([[n] * shape[1] for _ in range(shape[0])])

    @staticmethod
    def zeros(shape: tuple[int, int]) -> Matrix:
        """
        Creates a matrix of a given shape filled with zeros.
        """
        return Matrix.full(0, shape)

    @staticmethod
    def ones(shape: tuple[int, int]) -> Matrix:
        """
        Creates a matrix of a given shape filled with ones.
        """
        return Matrix.full(1, shape)

    @staticmethod
    def eye(n: int) -> Matrix:
        """
        Creates an identity matrix of size n x n.

        Args:
            n (int): The size of the matrix (rows and columns).

        Returns:
            Matrix: An identity matrix.
        """
        matrix = Matrix.zeros((n, n))
        for i in range(n):
            matrix[i, i] = 1
        return matrix

    @property
    def shape(self) -> tuple[int, int]:
        """
        Returns the shape of the matrix as (rows, columns).
        """
        return len(self.matrix), len(self.matrix[0])

    def clone(self) -> Matrix:
        """
        Creates a deep copy of the matrix.
        """
        return Matrix(copy.deepcopy(self.matrix))

    def __getitem__(self, key: tuple[int, int]) -> int:
        """
        Allows access to matrix elements using m[row, col].
        """
        return self.matrix[key[0]][key[1]]

    def __setitem__(self, key: tuple[int, int], value: int) -> None:
        """
        Allows setting matrix elements using m[row, col] = value.
        """
        self.matrix[key[0]][key[1]] = value

    def __matmul__(self, other: Matrix) -> Matrix:
        """
        Implements matrix multiplication using the @ operator.
        Performs the operation (A * B) % MOD.

        Args:
            other (Matrix): The matrix to multiply with.

        Returns:
            Matrix: The result of the multiplication.
        """
        rows_a, cols_a = self.shape
        rows_b, cols_b = other.shape

        assert cols_a == rows_b, "Matrix dimensions do not match for multiplication."

        result = self.zeros((rows_a, cols_b))

        for i in range(rows_a):
            for j in range(cols_b):
                val = 0
                for k in range(cols_a):
                    val += self[i, k] * other[k, j]
                    # Note: Applying modulo at each addition prevents overflow
                    # and keeps numbers small for efficiency.
                    val %= self.MOD
                result[i, j] = val

        return result

    def __pow__(self, n: int) -> Matrix:
        """
        Implements matrix exponentiation using the ** operator.
        Uses the Binary Exponentiation (Divide and Conquer) algorithm
        to achieve O(log n) time complexity.

        Args:
            n (int): The exponent.

        Returns:
            Matrix: The result of self ** n.
        """
        if n == 0:
            # Note: A matrix to the power of 0 is the Identity Matrix.
            return self.eye(self.shape[0])
        elif n == 1:
            return self

        half = self.__pow__(n // 2)

        if n % 2 == 0:
            # Even power: A^n = A^(n/2) * A^(n/2)
            return half @ half
        else:
            # Odd power: A^n = A^(n/2) * A^(n/2) * A
            return half @ half @ self

    def __repr__(self) -> str:
        """
        Returns a string representation of the matrix.
        Rows are separated by newlines, elements by spaces.
        """
        return '\n'.join(' '.join(map(str, row)) for row in self.matrix)