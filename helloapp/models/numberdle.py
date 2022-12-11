import random


class Numberdle:
    secret_numbers = []
    player_guesses = []
    board = []  # board is made up of 5 rows
    guesses = 0

    def asses_guess(self, player_guess):
        print("player_guess:" + str(player_guess))
        print(self.secret_numbers)
        row = []
        for x in range(5):
            print("x:" + str(x))
            secret_number = self.secret_numbers[x]
            print("secret_number:" + str(secret_number))
            if player_guess == secret_number:
                row.append('=' + str(secret_number))
            elif player_guess > secret_number:
                row.append('>')
            else:
                row.append('<')
        print(row)

        self.board.append(row)
        print(self.board)

    def __init__(self):
        print("init called")
        self.secret_numbers = []
        for x in range(5):
            self.secret_numbers.append(random.randint(1, 20))
        self.guesses = 0
        print(self.secret_numbers)

    def __str__(self):
        output = ""
        for row in self.board:
            for assessment in row:
                output = output + "..." + assessment
            output = output + "---"

        return output
