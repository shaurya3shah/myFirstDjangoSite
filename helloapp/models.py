# Create your models here.
import nltk
from nltk import word_tokenize


class GuessedNumber:
    guessed_number = int
    comparison = str

    def __str__(self):
        return str(self.guessed_number) + ' is' + self.comparison + ' than the secret number'


class CrazyLibs:
    initial_text = str
    added_story = str
    created_story = str
    pos_tagged_text = []
    nouns = []
    verbs = []
    adjectives = []

    def __str__(self):
        return self.initial_text + ' : ' + self.added_story

    def tokenize(self):

        self.nouns.__init__(self.nouns)
        self.verbs.__init__(self.verbs)
        self.adjectives.__init__(self.adjectives)

        words = word_tokenize(self.original_story(self))
        self.pos_tagged_text = nltk.pos_tag(words)

        # nltk.help.upenn_tagset(pos_tag_word[1])
        # https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
        for pos_tag_word in self.pos_tagged_text:
            print(pos_tag_word[0], ":", pos_tag_word[1])
            match pos_tag_word[1]:
                case 'NN':
                    self.nouns.append(pos_tag_word[0])
                case 'VB':
                    self.verbs.append(pos_tag_word[0])
                case 'JJ':
                    self.adjectives.append(pos_tag_word[0])

    def original_story(self):
        return self.initial_text + " " + self.added_story
