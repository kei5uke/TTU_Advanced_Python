from difflib import unified_diff
import sys
sys.path.append('../triangle_kekonn/')
from calculate import calculate
import unittest

"""
https://test.pypi.org/project/triangle-kekonn/0.0.3/
"""

class TestCalc(unittest.TestCase):
    def test_calculation(self):
        self.assertEqual(calculate(1, 2), 1, "Should be 1")
        self.assertEqual(calculate(100, 200), 10000, "Should be 1000")
        self.assertEqual(calculate(1000000, 2000000), 1000000000000, "Should be 1500000")
        self.assertEqual(calculate(1.5, 2), 1.5, "Should be 1.5")
        self.assertFalse

    def test_rise_error(self):
        try:
            calculate(-1, 10)
        except:
            pass
        else:
            raise self.assertRaises()

if __name__ == "__main__":
    unittest.main()