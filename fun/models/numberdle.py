import random


class Numberdle:
    secret_numbers = []
    successful_guesses = []
    board = []  # board is made up of 5 rows
    guesses = 0
    correct_guesses = 0

    def asses_guess(self, player_guess):
        print("player_guess:" + str(player_guess))
        print(self.secret_numbers)
        row = [player_guess]
        for x in range(1, 6):
            print("x:" + str(x))
            secret_number = self.secret_numbers[x-1]
            print("secret_number:" + str(secret_number))
            if self.successful_guesses[x-1] != 'N':
                row.append(self.successful_guesses[x-1])
            elif player_guess == secret_number:
                row.append('=' + str(secret_number))
                self.successful_guesses[x-1] = '=' + str(secret_number)
                self.correct_guesses += 1
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
        self.successful_guesses = []
        for x in range(5):
            self.secret_numbers.append(random.randint(1, 20))
            self.successful_guesses.append('N')
        self.guesses = 0
        self.board = []
        self.correct_guesses = 0
        print(self.secret_numbers)

    def __str__(self):
        output = ""
        for row in self.board:
            for assessment in row:
                output = output + "..." + assessment
            output = output + "---"

        return output
