import sys
sys.path.append('../triangle_kekonn/')
from calculate import calculate

"""
https://test.pypi.org/project/triangle-kekonn/0.0.3/
"""

def test_calc():
    assert calculate(1, 2) == 1, "Should be 1"
    assert calculate(100, 200) == 10000, "Should be 1000"
    assert calculate(1000000, 2000000) == 1000000000000, "Should be 1500000"
    assert calculate(1.5, 2) == 1.5, "Should be 1.5"

if __name__ == "__main__":
    test_calc()
    print("Test Cases Passed")