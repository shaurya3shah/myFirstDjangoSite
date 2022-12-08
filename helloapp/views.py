import random
import nltk

# Create your views here.
from django.http import HttpResponse
from django.template import loader

from helloapp.crazyLibs import generate_original_libs
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

    crazyLibsObj = generate_original_libs()
    crazyLibsObj.tokenize(crazyLibsObj)

    context = {'story': crazyLibsObj.original_story(crazyLibsObj), 'nouns': crazyLibsObj.nouns,
               'verbs': crazyLibsObj.verbs, 'adjectives': crazyLibsObj.adjectives}

    request.session['crazyLibsObj'] = crazyLibsObj
    print("setting session crazyLibsObj: " + str(crazyLibsObj.__str__(crazyLibsObj)))
    return HttpResponse(template.render(context, request))


def generate_crazy_libs(request):
    template = loader.get_template('helloapp/crazylibs.html')
    crazyLibsObj = request.session['crazyLibsObj']
    print("received session crazyLibsObj: " + str(crazyLibsObj.__str__(crazyLibsObj)))

    for noun in crazyLibsObj.nouns:
        input_noun = str(request.POST.get("input_noun_" + noun))
        print("input_noun_" + noun + ": " + input_noun)
        if input_noun != '' and len(input_noun) > 2:
            crazyLibsObj.make_crazy(crazyLibsObj, noun, input_noun)

    for verb in crazyLibsObj.verbs:
        input_verb = str(request.POST.get("input_verb_" + verb))
        print("input_verb_" + verb + ": " + input_verb)
        if input_verb != '' and len(input_verb) > 2:
            crazyLibsObj.make_crazy(crazyLibsObj, verb, input_verb)

    for adjective in crazyLibsObj.adjectives:
        input_adjective = str(request.POST.get("input_adjective_" + adjective))
        print("input_adjective_" + adjective + ": " + input_adjective)
        if input_adjective != '' and len(input_adjective) > 2:
            crazyLibsObj.make_crazy(crazyLibsObj, adjective, input_adjective)

    print("The final crazy story is" + crazyLibsObj.crazy_story)
    request.session['crazyLibsObj'] = crazyLibsObj

    print("setting session crazyLibsObj: " + str(crazyLibsObj.__str__(crazyLibsObj)))

    context = {'crazyLibsObj': crazyLibsObj}

    return HttpResponse(template.render(context, request))
