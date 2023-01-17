import unittest

from myFirstDjangoSite.settings import connection


class MyTestCase(unittest.TestCase):
    def test_something(self):
        superStarQuery = "select day1.Date as day1_date,  day1.Ticker as day1_ticker, day1.Performance as " \
                         "day1_performance," \
                         "day2.Date as day2_date,  day2.Ticker as day2_ticker, day2.Performance as day2_performance," \
                         "day3.Date as day3_date,  day3.Ticker as day3_ticker, day3.Performance as day3_performance " \
                         "from  snp_performance_2023_01_11 as day1 inner join snp_performance_2023_01_12 day2 " \
                         "on day1.Ticker = day2.Ticker and day1.Performance > 3 and day2.Performance > 3 " \
                         "inner join snp_performance_2023_01_13 as day3 on day2.Ticker = day3.Ticker and " \
                         "day3.Performance > 3; "
        result = connection.execute(superStarQuery)

        for row in result.fetchall():
            print(row)
            print(row['day1_date'])
            print(row['day1_ticker'])
            print(row['day1_performance'])
            print(row['day2_date'])
            print(row['day2_ticker'])
            print(row['day2_performance'])
            print(row['day3_date'])
            print(row['day3_ticker'])
            print(row['day3_performance'])
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
