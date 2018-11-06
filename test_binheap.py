import unittest
from BinomialHeap import BinomialHeap

class TestDict(unittest.TestCase):

    def test_get(self):

        binHeap = BinomialHeap()
        binHeap.add(1, "hi")
        binHeap.add(2, "hel")
        binHeap.add(3, "ther")
        binHeap.add(4, "asdf")
        binHeap.add(5, "asdfasd")
        binHeap.add(7, "asdjfa")

        self.assertEqual("ther",binHeap.get(3).getValue())
        self.assertEqual("asdf",binHeap.get(4).getValue())
        self.assertEqual("hi",binHeap.get(1).getValue())
        self.assertEqual("asdjfa",binHeap.get(7).getValue())
        self.assertIsNone(binHeap.get(100))


if __name__ == "__main__":
    unittest.main()
