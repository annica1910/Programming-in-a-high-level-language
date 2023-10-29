"""
Array class for assignment 2
"""

import statistics
from itertools import chain


class Array:
    array = []
    MAX_cols = 0
    MAX_rows = 1
    total = 0

    def __init__(self, shape, *values):
        # Set instance attributes
        self.values = values
        self.shape = shape
        self.dim = len(shape)
        self.MAX_cols = shape[0]
        if len(shape) > 1:
            self.MAX_rows = shape[1]
        self.total = self.MAX_cols*self.MAX_rows
        
        # Check if the args are valid types
        if not (type(shape) or type(values)) is tuple:
            raise TypeError("Args are of wrong type!")

        # Check if the values are of valid types
        if not all([isinstance(value, (int, float, bool)) for value in values]):
            raise ValueError("Only int, float, bool values allowed")

        # Check that the amount of values corresponds to the shape
        if self.total != len(values):            
            raise ValueError("Amount of values does not fit in given shape")

        idx = 0
        arr = []
        if self.n_dim():   #2D, har ikke simpl for nD
            for i in range(self.MAX_rows):
                row = []
                for j in range(self.MAX_cols):
                    row.append(values[idx])
                    idx += 1
                arr.append(row)
        else:   #1D
            arr = list(values)

        self.array = arr
        """Initialize an array of 1-dimensionality. Elements can only be of type:

        - int
        - float
        - bool

        Make sure the values and shape are of the correct type.

        Make sure that you check that your array actually is an array, which means it is homogeneous (one data type).

        Args:
            shape (tuple): shape of the array as a tuple. A 1D array with n elements will have shape = (n,).
            *values: The values in the array. These should all be the same data type. Either int, float or boolean.

        Raises:
            TypeError: If "shape" or "values" are of the wrong type.
            ValueError: If the values are not all of the same type.
            ValueError: If the number of values does not fit with the shape.
        """
    #løste 2d uten å flate ut array
    def flat_array(self):
        """Flattens the N-dimensional array of values into a 1-dimensional array.
        Returns:
            list: flat list of array values.
        """
        flat_array = self.array
        for _ in range(len(self.shape[1:])):
            flat_array = list(chain(*flat_array))
        return flat_array

    def getArray(self):
        return self.array
    
    def getValues(self):
        return self.values

    def getShape(self):
        return self.shape

    def getDim(self):
        return self.dim
    
    def n_dim(self):
        if self.dim > 1:
            return True
        return False

    def eq_shape(self, other):
        if self.getShape() == other.getShape():
            return True
        return False

    def __getitem__(self, index):
        return self.array[index]

    def __str__(self):
        """Returns a nicely printable string representation of the array.

        Returns:
            str: A string representation of the array.

        """
        string = ""
        if self.n_dim():
            for i in range(self.MAX_rows):
                for j in range(self.MAX_cols):
                    string += str(self.array[i][j])
        else:
            string = str(self.values)
        return string

    def __add__(self, other):
        """Element-wise adds Array with another Array or number.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to add element-wise to this array.

        Returns:
            Array: the sum as a new array.

        """
        # check that the method supports the given arguments (check for data type and shape of array)
        # if the array is a boolean you should return NotImplemented
        if isinstance(self.values[0], bool) or (not isinstance(other, (Array, int, float))):
            return NotImplemented

        if isinstance(other, Array):
            if not self.eq_shape(other):    #ulik shape
                return NotImplemented
            if self.n_dim():                #2d
                newArr = [[a + b for a, b in zip(i, j)] for i, j in zip(self.getArray(), other.getArray())]
            else:                           #1d
                newArr = [a + b for a, b in zip(self.values, other.getValues())]
                
        else:
            if self.n_dim():
                newArr = [[value + other for value in i] for i in self.getArray()]
            else:
                newArr = [self.values[i] + other for i in range(self.total)]

        return newArr
    
    def add_dim(self, i, j, dim, newA):
        if dim == 0:
            return newA
        else:
            count = 0
            for a, b in zip(i, j):
                if type(a) == list:
                    newA[count] = a + b
                count += 1
            dim-= 1
            
    def __radd__(self, other):
        """Element-wise adds Array with another Array or number.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to add element-wise to this array.

        Returns:
            Array: the sum as a new array.

        """
        return self.__add__(other)

    def __sub__(self, other):
        """Element-wise subtracts an Array or number from this Array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to subtract element-wise from this array.

        Returns:
            Array: the difference as a new array.

        """
        if isinstance(self.values[0], bool) or (not isinstance(other, (Array, int, float))):
            return NotImplemented
            (self.shape != other.getShape())
        if isinstance(other, Array):
            if not self.eq_shape(other):
                return NotImplemented
            if self.n_dim():
                newArr = [[a - b for a, b in zip(i, j)] for i, j in zip(self.getArray(), other.getArray())]
            else:
                newArr = [a - b for a, b in zip(self.values, other.getValues())]
                
        else:
            if self.n_dim():
                newArr = [[value - other for value in zip(i, j)] for i, j in self.getArray()]
            else:
                newArr = [self.values[i] - other for i in range(self.total)]
        return newArr

    def __rsub__(self, other):
        """Element-wise subtracts this Array from a number or Array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number being subtracted from.

        Returns:
            Array: the difference as a new array.

        """
        return self.__sub__(other)

    def __mul__(self, other):
        """Element-wise multiplies this Array with a number or array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to multiply element-wise to this array.

        Returns:
            Array: a new array with every element multiplied with `other`.

        """
        if isinstance(self.values[0], bool) or (not isinstance(other, (Array, int, float))):
            return NotImplemented
            (self.shape != other.getShape())
        if isinstance(other, Array):
            if not self.eq_shape(other):
                return NotImplemented
            if self.n_dim():
                newArr = [[a * b for a, b in zip(i, j)] for i, j in zip(self.getArray(), other.getArray())]
            else:
                newArr = [a * b for a, b in zip(self.values, other.getValues())]
        else:
            if self.n_dim():
                newArr = [[value * other for value in i] for i in self.getArray()]
            else:
                newArr = [self.values[i] * other for i in range(self.total)]
        return newArr

    def __rmul__(self, other):
        """Element-wise multiplies this Array with a number or array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to multiply element-wise to this array.

        Returns:
            Array: a new array with every element multiplied with `other`.

        """

        return self.__mul__(other)

    def eq_values(self, a, b):
        if a == b:
            return True
        return False

    def __eq__(self, other):
        """Compares an Array with another Array.

        If the two array shapes do not match, it should return False.
        If `other` is an unexpected type, return False.

        Args:
            other (Array): The array to compare with this array.

        Returns:
            bool: True if the two arrays are equal (identical). False otherwise.

        """
        
        if not isinstance(other, Array) or not self.eq_shape(other):
            return False
        for i, j in zip(self.getArray(), other.getArray()):
            if self.n_dim():
                for a, b in zip(i, j):
                    if a != b:
                        return False
            else:
                if i != j:
                    return False
        return True

    def is_equal(self, other):
        """Compares an Array element-wise with another Array or number.

        If `other` is an array and the two array shapes do not match, this method should raise ValueError.
        If `other` is not an array or a number, it should return TypeError.

        Args:
            other (Array, float, int): The array or number to compare with this array.

        Returns:
            Array: An array of booleans with True where the two arrays match and False where they do not.
                   Or if `other` is a number, it returns True where the array is equal to the number and False
                   where it is not.

        Raises:
            ValueError: if the shape of self and other are not equal.

        """
        if isinstance(other, (Array)):
            if not self.eq_shape(other):
                raise ValueError("Shape not match")
            if self.n_dim():
                newArr = [[self.eq_values(a,b) for a, b in zip(i, j)] for i, j in zip(self.getArray(), other.getArray())]
            else:
                newArr = [self.eq_values(a,b) for a, b in zip(self.getArray(), other.getArray())]
        elif isinstance(other, (int, float)):
            if self.n_dim():
                newArr = [[self.eq_values(a, other) for a in i] for i in self.getArray()]
            else:
                newArr = [self.eq_values(a, other) for a in self.getArray()]
        else:
            raise TypeError("Invalid type for arg")
        return newArr

    def min_element(self):
        """Returns the smallest value of the array.

        Only needs to work for type int and float (not boolean).

        Returns:
            float: The value of the smallest element in the array.

        """
        return min(self.getValues())  

    def mean_element(self):
        """Returns the mean value of an array

        Only needs to work for type int and float (not boolean).

        Returns:
            float: the mean value
        """
        return statistics.mean(self.getValues())
