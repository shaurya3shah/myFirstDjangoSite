import random
import nltk

# Create your views here.
from django.http import HttpResponse
from django.template import loader

from helloapp.crazyLibs import generate_crazy_libs
from helloapp.models import GuessedNumber
from helloapp.models import CrazyLibs

from nltk.tokenize import word_tokenize

secret_number: int = 0
check_count: int = 0


def index(request):
    template = loader.get_template('helloapp/index.html')
    global secret_number
    global check_count

    check_count = 0
    secret_number = random.randint(1, 100)

    context = {'secret_number': secret_number}

    return HttpResponse(template.render(context, request))


def check_guess(request):
    template = loader.get_template('helloapp/index.html')
    number = int(request.POST["Enter Your Guess"])
    user_guess = GuessedNumber
    user_guess.guessed_number = number
    global secret_number
    global check_count
    if user_guess.guessed_number < secret_number:
        user_guess.comparison = 'lesser'
    elif user_guess.guessed_number > secret_number:
        user_guess.comparison = 'greater'
    else:
        user_guess.comparison = 'equal'

    check_count += 1
    context = {'user_guess': user_guess, 'guess_count': check_count}

    return HttpResponse(template.render(context, request))


def crazy_libs(request):
    template = loader.get_template('helloapp/crazylibs.html')

    crazyLibsObj = CrazyLibs()
    crazyLibsObj = generate_crazy_libs()
    crazyLibsObj.tokenize(crazyLibsObj)

    context = {'story': crazyLibsObj.original_story(crazyLibsObj), 'nouns': crazyLibsObj.nouns,
               'verbs': crazyLibsObj.verbs, 'adjectives': crazyLibsObj.adjectives}
    return HttpResponse(template.render(context, request))
