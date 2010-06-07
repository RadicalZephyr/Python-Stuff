# Unit tests for hdi module

import unittest, hdi

class fluffTester(unittest.TestCase):
    def setUp(self):
        self.htmlfile = open(r'C:\Users\Geoff\prog\py\projects\hdi\testing.html', 'r')
        self.htmlstring = self.htmlfile.read()

    def tearDown(self):
        self.htmlfile.close()

    def testFluff(self):
        result = hdi.stripFluff(self.htmlstring)
        with open(r'C:\Users\Geoff\prog\py\projects\hdi\fluffcheck.txt') as check:
            self.assertEqual(result, check.read().upper())

class acTester(unittest.TestCase):
    def setUp(self):
        self.htmlfile = open(r'C:\Users\Geoff\prog\py\projects\hdi\html.txt')
        self.htmlstring = self.htmlfile.read()

    def tearDown(self):
        self.htmlfile.close()
    
    def testAddContent(self):
        content = 'This should appear.'
        result = hdi.addContent(content, self.htmlstring)
        with open(r'C:\Users\Geoff\prog\py\projects\hdi\addcontentcheck.txt') as checkfile:
            self.assertEqual(result, checkfile.read())


if __name__ == '__main__':
    unittest.main()