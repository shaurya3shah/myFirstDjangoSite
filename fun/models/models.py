# Create your models here.
import random
import time

import nltk
from nltk import word_tokenize

from fun.contentGeneratorAI import generate_original_libs, initiate_story
from myFirstDjangoSite.constants import TABLE_NAME_CRAZYLIBS
from myFirstDjangoSite.settings import client, ddb_exceptions, dynamodb
from django.db import models


class CrazyLibs:
    initial_text = str
    added_story = str
    crazy_story = ""
    pos_tagged_text = []
    nouns = []
    verbs = []
    adjectives = []

    def __str__(self):
        return str(self.initial_text) + ' ' + str(self.added_story)

    def tokenize(self):

        self.nouns.__init__(self.nouns)
        self.verbs.__init__(self.verbs)
        self.adjectives.__init__(self.adjectives)

        words = word_tokenize(self.original_story())
        self.pos_tagged_text = nltk.pos_tag(words)

        # nltk.help.upenn_tagset(pos_tag_word[1])
        # https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
        for pos_tag_word in self.pos_tagged_text:
            # print(pos_tag_word[0], ":", pos_tag_word[1])
            if pos_tag_word[1] == 'NN':
                    if pos_tag_word[0] not in self.nouns:
                        self.nouns.append(pos_tag_word[0])
            elif pos_tag_word[1] == 'VB':
                    if pos_tag_word[0] not in self.verbs:
                        self.verbs.append(pos_tag_word[0])
            elif pos_tag_word[1] == 'JJ':
                    if pos_tag_word[0] not in self.adjectives:
                        self.adjectives.append(pos_tag_word[0])

        self.limitInputWords()

    def limitInputWords(self):
        limit = 5
        if len(self.nouns) < limit:
            limit = len(self.nouns)

        self.nouns = random.choices(self.nouns, k=limit)

        limit = 5
        if len(self.verbs) < limit:
            limit = len(self.verbs)

        self.verbs = random.choices(self.verbs, k=limit)

        limit = 5
        if len(self.adjectives) < limit:
            limit = len(self.adjectives)

        self.adjectives = random.choices(self.adjectives, k=limit)


    def original_story(self):
        return str(self.initial_text) + " " + str(self.added_story)

    def make_crazy(self, item, input_item):
        print("noun: " + item + " input_item: " + input_item)
        if not self.crazy_story:
            self.crazy_story = str(self.initial_text) + " " + str(self.added_story)
        if input_item != '':
            self.crazy_story = self.crazy_story.replace(str(item),
                                                        '<span style="color: green; "><u>' + str(
                                                            input_item) + '</u></span>')

        self.initial_text = self.initial_text.replace(str(item),
                                                      '<span style="color: green; ">' + str(item) + '</span>')
        self.added_story = self.added_story.replace(str(item), '<span style="color: green; ">' + str(item) + '</span>')

        print("crazy story is: " + self.crazy_story)
        # https://stackoverflow.com/questions/50398901/python-django-change-font-color-for-part-of-string-found-in-another-list
        # https://stackoverflow.com/questions/21483003/replacing-a-character-in-django-template

    def addResult(self, user_id):
        try:
            response = client.put_item(
                TableName=TABLE_NAME_CRAZYLIBS,
                Item={
                    "timestamp": {"N": str(time.time())},
                    "user_id": {"N": str(user_id)},
                    "nouns": {"S": str(self.nouns)},
                    "adjectives": {"S": str(self.adjectives)},
                    "verbs": {"S": str(self.verbs)},
                    "initial_text": {"S": str(self.initial_text)},
                    "added_story": {"S": str(self.added_story)},
                    "crazy_story": {"S": str(self.crazy_story)}
                },
            )
            print(response)
        except ddb_exceptions:
            print(str(ddb_exceptions))

    def getStats(self):
        response = dynamodb.Table(TABLE_NAME_CRAZYLIBS).scan()
        print(response)
        return response.get('Items')

    def __init__(self):
        self.initial_text = initiate_story()
        self.added_story = generate_original_libs(self.initial_text)
        self.crazy_story = ""


class Speech(models.Model):
    text = models.TextField(max_length=2000)
    language = models.TextField(max_length=50)
    file_name = models.TextField(max_length=1000)
