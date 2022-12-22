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
    crazy_story = ""
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
            # print(pos_tag_word[0], ":", pos_tag_word[1])
            match pos_tag_word[1]:
                case 'NN':
                    if pos_tag_word[0] not in self.nouns:
                        self.nouns.append(pos_tag_word[0])
                case 'VB':
                    if pos_tag_word[0] not in self.verbs:
                        self.verbs.append(pos_tag_word[0])
                case 'JJ':
                    if pos_tag_word[0] not in self.adjectives:
                        self.adjectives.append(pos_tag_word[0])

    def original_story(self):
        return self.initial_text + " " + self.added_story

    def make_crazy(self, item, input_item):
        print("noun: " + item + " input_item: " + input_item)
        if not self.crazy_story:
            self.crazy_story = self.initial_text + " " + self.added_story
        if input_item != '':
            self.crazy_story = self.crazy_story.replace(item, '<span style="color: green; "><u>' + input_item + '</u></span>')

        self.initial_text = self.initial_text.replace(item, '<span style="color: green; ">' + item + '</span>')
        self.added_story = self.added_story.replace(item, '<span style="color: green; ">' + item + '</span>')

        print("crazy story is: " + self.crazy_story)
        #https://stackoverflow.com/questions/50398901/python-django-change-font-color-for-part-of-string-found-in-another-list
        #https://stackoverflow.com/questions/21483003/replacing-a-character-in-django-template
