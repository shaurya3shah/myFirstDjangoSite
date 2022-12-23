import pandas


class HelpView:
    user_guesses = []
    counts = None

    def getUserGuessesAndCounts(self, stats):
        self.user_guesses = []
        self.counts = None
        df = pandas.DataFrame(stats)
        print(df)
        groupeddf = df.groupby(['tries'])['tries'].count().reset_index(name="count")
        print(groupeddf)
        tries = groupeddf['tries'].tolist()
        self.counts = groupeddf['count'].tolist()

        for x in tries:
            self.user_guesses.append(str(x) + ' guesses')
            print(x)

        print('Printing user_guesses & counts')
        print(self.user_guesses)
        print(self.counts)
