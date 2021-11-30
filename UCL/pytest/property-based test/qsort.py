import unittest
from unittest import result

from hypothesis import given, note, example
from hypothesis.strategies import lists, integers

def qSort(a, p, r):
    if p<r:
        q = partition(a, p, r)
        qSort(a, p, q-1)
        qSort(a, q+1, r)

def partition(a, p, r):
    x = a[r]

    i = p-1
    temp = 0

    for j in range(p, r):
        if a[j] <= x:
            i = i + 1
            temp = a[i]
            a[i] = a[j]
            a[j] = temp
    
    temp = a[i+1]
    a[i+1] = a[r]
    a[r] = temp

    return (i+1)

class TestSort(unittest.TestCase):

    @given(lists(integers()))
    @example([0, 1])
    def test_sorting_list_of_integers(self, numbers):
        qSort(numbers, 0, len(numbers)-1)
        note(f"sorted: {numbers}")
        self.assertTrue(all(x <= y for x, y in zip(numbers, numbers[1:])))

@given(lists(integers(0,1000)))
def test(numbers):
    assume(all(x>0 for x in numbers))
    result = sorted(numbers)
    assert(all(x <= y for x, y in zip(numbers, numbers[1:])))

if __name__ == "__main__":
    unittest.main()

    test()