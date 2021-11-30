import unittest
from prime_factors import prime_factors

class TestPrimeFactors(unittest.TestCase):
    def test_one(self):
        self.assertEqual(prime_factors(1), [])
    
    def test_two(self):
        self.assertEqual(prime_factors(2), [2])

    def test_six(self):
        self.assertEqual(prime_factors(6), [2,3])

if __name__ == "__main__":
    unittest.main()