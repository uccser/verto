
import unittest

def fun(x):
    return x + 1

class TestGlossaryLinks(unittest.TestCase):
    def test(self):
        self.assertEqual(fun(3), 4)
        self.assertEqual(fun(2), 4)
