import unittest

import pandas

from fun.models.guessNumber import GuessNumber


class MyTestCase(unittest.TestCase):

    def test_getStats(self):
        guessNumber = GuessNumber()
        stats = guessNumber.getStats()

        df = pandas.DataFrame(stats)

        print(df)

        groupeddf = df.groupby(['tries'])['tries'].count().reset_index(name="count")
        print(groupeddf)
        tries = groupeddf['tries'].tolist()
        count = groupeddf['count'].tolist()

        print('Printing Tries')
        print(tries)
        user_guesses = []
        for x in tries:
            user_guesses.append(str(x) + ' guesses')
            print(x)

        print('Printing user_guesses')
        print(user_guesses)

        print('Printing Counts')
        print(count)
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
