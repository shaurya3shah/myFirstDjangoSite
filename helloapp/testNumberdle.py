import unittest

from helloapp.models.numberdle import Numberdle


class TestNumberdle(unittest.TestCase):
    def test_print_board(self):
        numberdle = Numberdle()
        print(str(numberdle))
        self.assertEqual(True, True)  # add assertion here

    def test_init(self):
        numberdle = Numberdle()
        print(numberdle.secret_numbers)
        self.assertEqual(True, True)  # add assertion here

if __name__ == '__main__':
    unittest.main()