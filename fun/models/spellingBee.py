import random

from fun.spelling_bee_practise_graph import dynamo_db_to_list


class SpellingBee:
    current_word = ''
    user_input = ''
    word_list = []
    array_counter = 0
    tries = []
    correct_counter = 0
    correct = []
    incorrect_counter = 0
    incorrect = []

    def getNewWord(self):
        print('before - current_word: ' + self.current_word)
        self.current_word = self.word_list[random.randint(0, 99)]['word']
        print('after - current_word: ' + self.current_word)
        return self.current_word

    def spellCheck(self, input_word):
        print('current_word: ' + self.current_word + ' input_word: ' + input_word)
        self.user_input = input_word.lower().strip()

        if self.user_input == self.current_word.lower().strip():
            self.recordCorrect()
            return True
        else:
            self.recordIncorrect()
            return False

    def recordCorrect(self):
        old_correct = self.correct[self.array_counter]
        old_incorrect = self.incorrect[self.array_counter]
        self.array_counter += 1
        self.tries.append(self.array_counter)
        self.correct.append(old_correct + 1)
        self.incorrect.append(old_incorrect)

    def recordIncorrect(self):
        old_correct = self.correct[self.array_counter]
        old_incorrect = self.incorrect[self.array_counter]
        self.array_counter += 1
        self.tries.append(self.array_counter)
        self.correct.append(old_correct)
        self.incorrect.append(old_incorrect + 1)

    def __init__(self):
        self.word_list = dynamo_db_to_list()
        self.current_word = self.word_list[random.randint(0, 99)]['word']
        self.array_counter = 0
        self.tries = []
        self.tries.append(self.array_counter)
        self.correct = []
        self.correct.append(self.array_counter)
        self.incorrect = []
        self.incorrect.append(self.array_counter)

