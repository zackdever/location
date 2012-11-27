#!/usr/bin/env python

import unittest

class TestAPI(unittest.TestCase):

    def setUp(self):
        pass

    def test_fail(self):
        self.assertFalse(True, 'There are no tests...')

def test():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAPI)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    test()
