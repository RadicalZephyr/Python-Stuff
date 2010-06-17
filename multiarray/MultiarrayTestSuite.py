import unittest
from multiarray import *


class MultiArrayTester(unittest.TestCase):
    testCases = [ [0,0,0,0], [[0,0],[0,0]],
                  [[[0,0], [0,0]], [[0,0], [0,0]]],
                  [1,1,1,1] ]

    def setUp(self):
        self.ma = MultiArray(3,6)

    def tearDown(self):
        del self.ma

    def testConstructer(self):
        b = MultiArray(4)
        self.assertEqual(b.array, self.testCases[0])
        c = MultiArray(2,2)
        self.assertEqual(c.array, self.testCases[1])
        a = MultiArray(2, 2, 2)
        self.assertEqual(a.array, self.testCases[2])

    def testDefVal(self):
        defTest = MultiArray(4, defval=1)
        self.assertEqual(defTest.array, self.testCases[3])

    def testGetItem(self):
        for i in xrange(3):
            for j in xrange(6):
                self.assertEqual(self.ma[i, j], 0)

    def testSetItem(self):
        for i in xrange(3):
            for j in xrange(6):
                self.ma[i,j] = i+j
        for i in xrange(3):
            for j in xrange(6):
                self.assertEqual(self.ma[i,j], i+j)

if __name__ == "__main__":
    print
    unittest.main()