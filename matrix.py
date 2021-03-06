import math
from math import sqrt
import numbers

def zeroes(height, width):
        """
        Creates a matrix of zeroes.
        """
        g = [[0.0 for _ in range(width)] for __ in range(height)]
        return Matrix(g)

def identity(n):
        """
        Creates a n x n identity matrix.
        """
        I = zeroes(n, n)
        for i in range(n):
            I.g[i][i] = 1.0
        return I

    
def dot_product(vector_one, vector_two):

    dot_prod = 0
    
    for i in range(len(vector_one)):
            dot_prod += vector_one[i] * vector_two[i]
                
    return dot_prod
    
class Matrix(object):

    # Constructor
    def __init__(self, grid):
        self.g = grid
        self.h = len(grid)
        self.w = len(grid[0])

    #
    # Primary matrix math methods
    #############################
 
    def determinant(self):
        """
        Calculates the determinant of a 1x1 or 2x2 matrix.
        """
        det = 0.0
        
        if not self.is_square():
            raise(ValueError, "Cannot calculate determinant of non-square matrix.")
        if self.h > 2:
            raise(NotImplementedError, "Calculating determinant not implemented for matrices largerer than 2x2.")
        
        if self.h == 1:
            det = self[0][0]   
        else:
            a = self[0][0]
            b = self[0][1]
            c = self[1][0]
            d = self[1][1]
            
            
            det = (a * d - b * c)
            
        return det
    
    def trace(self):
        """
        Calculates the trace of a matrix (sum of diagonal entries).
        """
        trace = 0.0
        
        if not self.is_square():
            raise(ValueError, "Cannot calculate the trace of a non-square matrix.")
        
        
        for i in range(self.h):
            for j in range(self.w):
                if i == j:
                    trace = trace + self[i][j]
                           
        return trace

    def inverse(self):
        """
        Calculates the inverse of a 1x1 or 2x2 Matrix.
        """
        calculate_inverse = []
        inverse = []
        
        if not self.is_square():
            raise(ValueError, "Non-square Matrix does not have an inverse.")
        if self.h > 2:
            raise(NotImplementedError, "inversion not implemented for matrices larger than 2x2.")
        
        if self.h == 1:
            inverse.append([1/self[0][0]])
        elif self.h == 2:
            if self.determinant() == 0:
                raise ValueError('The matrix is not invertible.')
            else:
                det = 1/self.determinant()
                trace = self.trace()
                identity_matrix = identity(self.h)
                
                for i in range(self.h):
                    row = []
                    for j in range(self.w):
                        calculate_inverse = (trace*identity_matrix[i][j])-self[i][j]
                        row.append(calculate_inverse)
                    inverse.append(row)

                for i in range(len(inverse)):
                    for j in range(len(inverse[0])):
                        inverse[i][j] = det * inverse[i][j]
        
        return Matrix(inverse)

    def T(self):
        """
        Returns a transposed copy of this Matrix.
        """
        transpose = []
    
        for c in range(self.w):
            row = []
            for r in range(self.h):
                row.append(self[r][c])
            transpose.append(row)
    
        return Matrix(transpose)

    def is_square(self):
        return self.h == self.w

    #
    # Begin Operator Overloading
    ############################
    def __getitem__(self,idx):
        """
        Defines the behavior of using square brackets [] on instances
        of this class.

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > my_matrix[0]
          [1, 2]

        > my_matrix[0][0]
          1
        """
        return self.g[idx]

    def __repr__(self):
        """
        Defines the behavior of calling print on an instance of this class.
        """
        s = ""
        for row in self.g:
            s += " ".join(["{} ".format(x) for x in row])
            s += "\n"
        return s

    def __add__(self,other):
        """
        Defines the behavior of the + operator
        """
        matrixSum = []
        
        if self.h != other.h or self.w != other.w:
            raise(ValueError, "Matrices can only be added if the dimensions are the same") 
        
        for i in range(self.h):
            row = []
            for j in range(self.w):
                row.append(self[i][j] + other[i][j])
            matrixSum.append(row)
              
         
        return Matrix(matrixSum)

    def __neg__(self):
        """
        Defines the behavior of - operator (NOT subtraction)

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > negative  = -my_matrix
        > print(negative)
          -1.0  -2.0
          -3.0  -4.0
        """
        negation = []
        
        for i in range(self.h):
            row = []
            for j in range(self.w):
                to_neg = -1 * self[i][j]
                row.append(to_neg)
            negation.append(row)
        
        return Matrix(negation)
    
    def __sub__(self, other):
        """
        Defines the behavior of - operator (as subtraction)
        """
        matrixSub = []
        
        if self.h != other.h or self.w != other.w:
            raise(ValueError, "Matrices can only be subtracted if the dimensions are the same") 
        
        for i in range(self.h):
            row = []
            for j in range(self.w):
                row.append(self[i][j] - other[i][j])
            matrixSub.append(row)
         
        return Matrix(matrixSub)

    def __mul__(self, other):
        """
        Defines the behavior of * operator (matrix multiplication)
        """
        product = []
        dotproduct = 0
        
        transpose = other.T()
    
        for i in range(self.h):
            row = []
            for j in range(transpose.h):
                dotproduct = dot_product(self[i],transpose[j])
                row.append(dotproduct)
            product.append(row)
        
        return Matrix(product)

    def __rmul__(self, other):
        """
        Called when the thing on the left of the * is not a matrix.

        Example:

        > identity = Matrix([ [1,0], [0,1] ])
        > doubled  = 2 * identity
        > print(doubled)
          2.0  0.0
          0.0  2.0
        """
        product = []
        
        if isinstance(other, numbers.Number):
            for i in range(self.h):
                row = []
                for j in range(self.w):
                    scalar_multiplication = other * self[i][j]
                    row.append(scalar_multiplication)
                product.append(row)
      
        return Matrix(product)