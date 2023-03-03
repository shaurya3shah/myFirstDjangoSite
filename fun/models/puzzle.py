from fun.contentGeneratorAI import generatePuzzle


class Puzzle:
    question = str
    solution = str

    def getPuzzle(self):
        generated_puzzle = generatePuzzle()

        print(generated_puzzle)

        split = generated_puzzle.split('Solution:')

        if len(split) > 0:
            self.question = split[0]
            self.solution = split[1]

    def __str__(self):
        return 'Question = ' + str(self.question) + '\n Solution = ' + str(self.solution)
