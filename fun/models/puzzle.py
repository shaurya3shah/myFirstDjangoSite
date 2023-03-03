from fun.contentGeneratorAI import generatePuzzle, checkPuzzleAnswer


class Puzzle:
    question = str
    solution = str
    answer = str
    validation = str

    def getPuzzle(self):
        self.question = ''
        self.solution = ''
        self.answer = ''
        self.validation = ''

        generated_puzzle = generatePuzzle()

        print(generated_puzzle)

        split = generated_puzzle.split('Solution:')

        if len(split) > 0:
            self.question = split[0].strip()
            self.solution = split[1].strip()

    def validateAnswer(self):
        self.validation = checkPuzzleAnswer(self.question, self.answer).strip()

    def __str__(self):
        return 'Question = ' + str(self.question) \
               + '\n Solution = ' + str(self.solution) \
               + '\n Answer = ' + str(self.answer) \
               + '\n Validation = ' + str(self.validation)
