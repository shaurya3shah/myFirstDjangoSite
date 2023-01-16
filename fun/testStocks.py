import unittest

from myFirstDjangoSite.settings import connection


class MyTestCase(unittest.TestCase):
    def test_something(self):
        superStarQuery = "select jan11.Date as day1_date,  jan11.Ticker as day1_ticker, jan11.Performance as " \
                         "day1_performance," \
                         "jan12.Date as day2_date,  jan12.Ticker as day2_ticker, jan12.Performance as day2_performance," \
                         "jan13.Date as day3_date,  jan13.Ticker as day3_ticker, jan13.Performance as day3_performance " \
                         "from  snp_performance_2023_01_11 as jan11 inner join snp_performance_2023_01_12 jan12 " \
                         "on jan11.Ticker = jan12.Ticker and jan11.Performance > 3 and jan12.Performance > 3 " \
                         "inner join snp_performance_2023_01_13 as jan13 on jan12.Ticker = jan13.Ticker and " \
                         "jan13.Performance > 3; "
        result = connection.execute(superStarQuery)

        for row in result.fetchall():
            print(row)
            print(row['day1_date'])
            print(row['day1_ticker'])
            print(row['day1_performance'])
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
