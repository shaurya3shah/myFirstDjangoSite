import random


class Numberdle:
    secret_numbers = []
    player_guesses = []
    board = [] #board is made up of 5 rows
    guesses = 0

    def __int__(self):
        for x in range(5):
            self.secret_numbers[x] = random.randint(1, 20)
        self.guesses = 0

    def __str__(self):
        output = ""
        for row in self.board:
            for assessment in row:
                output = output + "..." + assessment
            output = output + "---"

        return output

    def asses_guess(self, player_guess):
        row = []
        for x in range(5):
            secret_number = self.secret_numbers[x]
            if player_guess == secret_number:
                row[x] = '=' + str(secret_number)
            elif player_guess > secret_number:
                row[x] = '>'
            else:
                row[x] = '<'

        self.board.append(row)
