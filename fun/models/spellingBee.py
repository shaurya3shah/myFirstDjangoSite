import random

from fun.spelling_bee_practise_graph import dynamo_db_to_list


class SpellingBee:
    current_word = ''
    user_input = ''
    word_list = []

    def getNewWord(self):
        print('before - current_word: ' + self.current_word)
        self.current_word = self.word_list[random.randint(0, 99)]['word']
        print('after - current_word: ' + self.current_word)
        return self.current_word

    def spellCheck(self, input_word):
        print('current_word: ' + self.current_word + ' input_word: ' + input_word)
        self.user_input = input_word.lower().strip()

        if self.user_input == self.current_word.lower().strip():
            return True
        else:
            return False

    def __init__(self):
        self.word_list = dynamo_db_to_list()
        self.current_word = self.word_list[random.randint(0, 99)]['word']

