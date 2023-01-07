import pandas


class HelpView:
    user_guesses = []
    user_scores = []
    counts = None

    def getUserGuessesAndCounts(self, stats):
        self.user_guesses = []
        self.counts = None
        try:
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
        except:
            print('Error')

    # the getUserScoresAndCounts and getUserGuessesAndCounts seems very similar
    # but they are kept seperate for simplicity
    def getUserScoresAndCounts(self, stats):
        self.user_scores = []
        self.counts = None
        try:
            df = pandas.DataFrame(stats)
            print(df)
            groupeddf = df.groupby(['score'])['score'].count().reset_index(name="count")
            print(groupeddf)
            scores = groupeddf['score'].tolist()
            self.counts = groupeddf['count'].tolist()

            for x in scores:
                self.user_scores.append('score ' + str(x))
                print(x)

            print('Printing user_scores & counts')
            print(self.user_scores)
            print(self.counts)
        except:
            print('Error')