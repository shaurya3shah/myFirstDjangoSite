import unittest

from fun.models.countriesConnection import CountriesConnection


class TestCountriesConnection(unittest.TestCase):
    def test_init(self):
        countries_connection_obj = CountriesConnection()
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
