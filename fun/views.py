import random

import pandas
# Create your views here.
from django.http import HttpResponse
from django.template import loader

from fun.crazyLibs import generate_original_libs
from fun.helpView import HelpView
from fun.models.countriesConnection import CountriesConnection
from fun.models.guessNumber import GuessNumber
from fun.models.models import GuessedNumber
from fun.models.numberdle import Numberdle
from myFirstDjangoSite.settings import env

secret_number: int = 0
check_count: int = 0


def index(request):
    template = loader.get_template('fun/index.html')
    welcome_message = 'My Fun Hub!'

    context = {'welcome_message': welcome_message}
    print(context)
    print('LOVE is ' + str(env('LOVE')))

    return HttpResponse(template.render(context, request))


def guess_number(request):
    template = loader.get_template('fun/guessnumber.html')
    global secret_number
    global check_count

    check_count = 0
    secret_number = random.randint(1, 100)

    context = {'secret_number': secret_number}

    return HttpResponse(template.render(context, request))


def check_guess(request):
    template = loader.get_template('fun/guessnumber.html')
    global secret_number
    global check_count
    helpView = HelpView()
    user_input = request.POST["Enter Your Guess"]

    if user_input.isdigit():
        number = int(user_input)
        user_guess = GuessedNumber
        user_guess.guessed_number = number

        check_count += 1

        if user_guess.guessed_number < secret_number:
            user_guess.comparison = 'lesser'
        elif user_guess.guessed_number > secret_number:
            user_guess.comparison = 'greater'
        else:
            user_guess.comparison = 'equal'
            guessNumber = GuessNumber()
            guessNumber.addResult(0, check_count)
            helpView.getUserGuessesAndCounts(guessNumber.getStats())

        context = {'user_guess': user_guess, 'guess_count': check_count, 'user_guesses': helpView.user_guesses, 'counts': helpView.counts}
    else:
        error_message = 'Please enter a number'
        context = {'error_message': error_message, 'guess_count': check_count}

    return HttpResponse(template.render(context, request))


def crazy_libs(request):
    template = loader.get_template('fun/crazylibs.html')

    crazyLibsObj = generate_original_libs()
    crazyLibsObj.tokenize(crazyLibsObj)

    context = {'story': crazyLibsObj.original_story(crazyLibsObj), 'nouns': crazyLibsObj.nouns,
               'verbs': crazyLibsObj.verbs, 'adjectives': crazyLibsObj.adjectives}

    request.session['crazyLibsObj'] = crazyLibsObj
    print("setting session crazyLibsObj: " + str(crazyLibsObj.__str__(crazyLibsObj)))
    return HttpResponse(template.render(context, request))


def generate_crazy_libs(request):
    template = loader.get_template('fun/crazylibs.html')
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


def numberdle(request):
    template = loader.get_template('fun/numberdle.html')
    welcome_message = 'Numberdle!'

    numberdle_obj = Numberdle()
    request.session['numberdle_obj'] = numberdle_obj
    context = {'welcome_message': welcome_message, 'numberdle_obj': numberdle_obj}
    print(numberdle_obj.secret_numbers)
    print(context)

    return HttpResponse(template.render(context, request))


def check_numberdle(request):
    template = loader.get_template('fun/numberdle.html')
    welcome_message = 'Numberdle!'
    numberdle_obj = request.session['numberdle_obj']
    helpView = HelpView()

    user_input = request.POST.get("player_guess")
    if user_input and user_input.isdigit():
        numberdle_obj.guesses += 1
        player_guess = int(user_input)

        print(numberdle_obj.secret_numbers)

        numberdle_obj.asses_guess(player_guess)

        if numberdle_obj.correct_guesses == 5:
            numberdle_obj.addResult(0)
            helpView.getUserGuessesAndCounts(numberdle_obj.getStats())

        request.session['numberdle_obj'] = numberdle_obj
        context = {'welcome_message': welcome_message, 'numberdle_obj': numberdle_obj, 'user_guesses': helpView.user_guesses, 'counts': helpView.counts}
        print(context)
    else:
        error_message = 'Please enter a number'
        context = {'error_message': error_message, 'welcome_message': welcome_message, 'numberdle_obj': numberdle_obj}

    return HttpResponse(template.render(context, request))


def countries_connection(request):
    template = loader.get_template('fun/countriesconnection.html')
    welcome_message = 'Countries Connection!'

    countries_connection_obj = CountriesConnection()
    request.session['countries_connection_obj'] = countries_connection_obj
    context = {'welcome_message': welcome_message, 'countries_connection_obj': countries_connection_obj}
    print(context)

    return HttpResponse(template.render(context, request))


def connect_country(request):
    template = loader.get_template('fun/countriesconnection.html')

    player_input = str(request.POST.get("Enter Country")).strip()

    countries_connection_obj = request.session['countries_connection_obj']

    result = countries_connection_obj.connect_country(player_input)

    request.session['countries_connection_obj'] = countries_connection_obj

    context = {'countries_connection_obj': countries_connection_obj, 'result': result}
    print(context)

    return HttpResponse(template.render(context, request))
