"""
Custom types for the language interpreter.
Includes Complex numbers and Matrix types.
"""

from typing import List, Any


class Complex:
    """
    Complex number type with real and imaginary parts.
    Supports basic arithmetic operations.
    """
    
    def __init__(self, real: float, imag: float):
        """
        Initialize a complex number.
        
        Args:
            real: Real part
            imag: Imaginary part
        """
        self.real = real
        self.imag = imag
    
    def __add__(self, other):
        """Addition with another complex or scalar."""
        if isinstance(other, Complex):
            return Complex(self.real + other.real, self.imag + other.imag)
        return Complex(self.real + other, self.imag)
    
    def __radd__(self, other):
        """Right addition (scalar + complex)."""
        return self.__add__(other)
    
    def __sub__(self, other):
        """Subtraction with another complex or scalar."""
        if isinstance(other, Complex):
            return Complex(self.real - other.real, self.imag - other.imag)
        return Complex(self.real - other, self.imag)
    
    def __rsub__(self, other):
        """Right subtraction (scalar - complex)."""
        if isinstance(other, Complex):
            return Complex(other.real - self.real, other.imag - self.imag)
        return Complex(other - self.real, -self.imag)
    
    def __mul__(self, other):
        """Multiplication with another complex or scalar."""
        if isinstance(other, Complex):
            return Complex(
                self.real * other.real - self.imag * other.imag,
                self.real * other.imag + self.imag * other.real
            )
        return Complex(self.real * other, self.imag * other)
    
    def __rmul__(self, other):
        """Right multiplication (scalar * complex)."""
        return self.__mul__(other)
    
    def __truediv__(self, other):
        """Division by another complex or scalar."""
        if isinstance(other, Complex):
            denom = other.real ** 2 + other.imag ** 2
            return Complex(
                (self.real * other.real + self.imag * other.imag) / denom,
                (self.imag * other.real - self.real * other.imag) / denom
            )
        return Complex(self.real / other, self.imag / other)
    
    def __neg__(self):
        """Negation."""
        return Complex(-self.real, -self.imag)
    
    def __abs__(self):
        """Absolute value (magnitude)."""
        return (self.real ** 2 + self.imag ** 2) ** 0.5
    
    def __eq__(self, other):
        """Equality comparison."""
        if isinstance(other, Complex):
            return self.real == other.real and self.imag == other.imag
        return False
    
    def __repr__(self):
        """String representation."""
        if self.imag >= 0:
            return f"{self.real}+{self.imag}i"
        return f"{self.real}{self.imag}i"
    
    def __str__(self):
        """String representation for printing."""
        return self.__repr__()


class Matrix:
    """
    Matrix type for 2D arrays.
    Supports basic matrix operations.
    """
    
    def __init__(self, rows: List[List[Any]]):
        """
        Initialize a matrix from rows.
        
        Args:
            rows: List of rows, each row is a list of values
        """
        self.rows = rows
        self.num_rows = len(rows)
        self.num_cols = len(rows[0]) if rows else 0
    
    def __getitem__(self, key):
        """Get element or row by index."""
        if isinstance(key, tuple):
            return self.rows[key[0]][key[1]]
        return self.rows[key]
    
    def __add__(self, other):
        """Matrix addition."""
        if isinstance(other, Matrix):
            if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
                raise ValueError("Matrix dimensions must match for addition")
            result = [
                [self.rows[i][j] + other.rows[i][j] for j in range(self.num_cols)]
                for i in range(self.num_rows)
            ]
            return Matrix(result)
        raise TypeError("Can only add matrix to matrix")
    
    def __sub__(self, other):
        """Matrix subtraction."""
        if isinstance(other, Matrix):
            if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
                raise ValueError("Matrix dimensions must match for subtraction")
            result = [
                [self.rows[i][j] - other.rows[i][j] for j in range(self.num_cols)]
                for i in range(self.num_rows)
            ]
            return Matrix(result)
        raise TypeError("Can only subtract matrix from matrix")
    
    def __mul__(self, other):
        """Matrix multiplication or scalar multiplication."""
        if isinstance(other, Matrix):
            if self.num_cols != other.num_rows:
                raise ValueError("Matrix dimensions incompatible for multiplication")
            result = [
                [
                    sum(self.rows[i][k] * other.rows[k][j] for k in range(self.num_cols))
                    for j in range(other.num_cols)
                ]
                for i in range(self.num_rows)
            ]
            return Matrix(result)
        # Scalar multiplication
        result = [
            [self.rows[i][j] * other for j in range(self.num_cols)]
            for i in range(self.num_rows)
        ]
        return Matrix(result)
    
    def __rmul__(self, other):
        """Right scalar multiplication."""
        return self.__mul__(other)
    
    def __neg__(self):
        """Negation of all elements."""
        return Matrix([[-x for x in row] for row in self.rows])
    
    def __eq__(self, other):
        """Equality comparison."""
        if isinstance(other, Matrix):
            return self.rows == other.rows
        return False
    
    def __repr__(self):
        """String representation."""
        row_strs = []
        for row in self.rows:
            row_strs.append("{" + ", ".join(str(x) for x in row) + "}")
        return "{" + ", ".join(row_strs) + "}"
    
    def __str__(self):
        """String representation for printing."""
        return self.__repr__()
    
    def transpose(self):
        """Return the transpose of the matrix."""
        result = [
            [self.rows[j][i] for j in range(self.num_rows)]
            for i in range(self.num_cols)
        ]
        return Matrix(result)
