"""
Tests for our array class
"""

from time import time
from array_class import Array

# 1D tests (Task 4)

def test_str_1d():
    assert array.__str__() == "(1, 2, 3, 4)"
    assert boolarray.__str__() == "(True, False, True)"
    assert floatarray.__str__() == "(1.1, 2.2, 3.3, 4.4)"

def test_add_1d():
    assert(array.__add__(1) == [2,3,4,5])
    assert(array.__add__(0.5) == [1.5, 2.5, 3.5, 4.5])
    assert(array.__add__(array) == [2, 4, 6 , 8])
    assert boolarray.__add__(boolarray) == NotImplemented
    assert array.__add__("Hei") == NotImplemented
    assert array.__add__(array4) == NotImplemented

def test_sub_1d():
    assert(array.__sub__(1) == [0,1,2,3])
    assert(array.__sub__(0.5) == [0.5, 1.5, 2.5, 3.5])
    assert(array.__sub__(array) == [0, 0, 0, 0])
    assert boolarray.__sub__(boolarray) == NotImplemented
    assert array.__sub__("Hei") == NotImplemented
    assert array.__sub__(array4) == NotImplemented

def test_mul_1d():
    assert(array.__mul__(2) == [2, 4, 6, 8])
    assert(array.__mul__(0.5) == [0.5, 1, 1.5, 2])
    assert boolarray.__mul__(boolarray) == NotImplemented
    assert array.__mul__("Hei") == NotImplemented
    assert array.__mul__(array4) == NotImplemented


def test_eq_1d():
    assert(array.__eq__(array) == True)
    assert(array.__eq__(arrayNotEq) == False)

def test_same_1d():
    assert array.is_equal(arrayNotEq) == [False, True, True, True]
    assert array.is_equal(2) == [False, True, False, False]
    assert array3.is_equal(2) == [True, True, True, True]

def test_smallest_1d():
    assert array.min_element() == 1
    assert arrayNotEq.min_element() == 2

def test_mean_1d():
    assert array.mean_element() == 2.5
    assert array3.mean_element() == 2


# 2D tests (Task 6)


def test_add_2d():
    assert(array2.__add__(1) == [[2, 3], [4, 5]])
    assert(array2.__add__(0.5) == [[1.5, 2.5], [3.5, 4.5]])
    assert(array2.__add__(array2) == [[2, 4], [6, 8]])


def test_mult_2d():
    assert(array2.__mul__(2) == [[2, 4], [6, 8]])
    assert(array2.__mul__(0.5) == [[0.5, 1], [1.5, 2]])
    assert(array2.__mul__(array2) == [[1, 4], [9, 16]])


def test_same_2d():
    array2NotEq = Array((2,2), 2,2,3,4)
    assert array2.is_equal(array2NotEq) == [[False, True], [True, True]]
    assert array2.is_equal(2) == [[False, True], [False, False]]
    assert array2NotEq.is_equal(2) == [[True, True], [False, False]]

def test_mean_2d():
    assert array2.mean_element() == 2.5

def test_getItem():
    assert array[0] == 1
    assert array2[1][0] == 3

if __name__ == "__main__":
    """
    Note: Write "pytest" in terminal in the same folder as this file is in to run all tests
    (or run them manually by running this file).
    Make sure to have pytest installed (pip install pytest, or install anaconda).
    """
    array = Array((4,), 1,2,3,4)
    array2 = Array((2,2), 1,2,3,4)
    arrayNotEq = Array((4,), 2,2,3,4)
    array3 = Array((4,), 2,2,2,2)
    array4 = Array((2,), 1,1)
    boolarray = Array((3,), True, False, True)
    floatarray = Array((4,), 1.1, 2.2, 3.3, 4.4)

    # Task 4: 1d tests
    test_str_1d()
    test_add_1d()
    test_sub_1d()
    test_mul_1d()
    test_eq_1d()
    test_mean_1d()
    test_same_1d()
    test_smallest_1d()

    # Task 6: 2d tests
    test_add_2d()
    test_mult_2d()
    test_same_2d()
    test_mean_2d()
    test_getItem()

    print("All tests done! 13/13 :)")
