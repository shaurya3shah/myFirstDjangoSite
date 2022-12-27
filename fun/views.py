import random

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from gtts.tts import gTTS

from fun.crazyLibs import generate_original_libs
from fun.helpView import HelpView
from fun.models.countriesConnection import CountriesConnection
from fun.models.guessNumber import GuessNumber
from fun.models.numberdle import Numberdle
from myFirstDjangoSite.settings import env


def index(request):
    template = loader.get_template('fun/index.html')
    welcome_message = 'My Fun Hub!'

    context = {'welcome_message': welcome_message}
    print(context)
    print('LOVE is ' + str(env('LOVE')))

    return HttpResponse(template.render(context, request))


def guess_number(request):
    template = loader.get_template('fun/guessnumber.html')
    secret_number = random.randint(1, 100)

    guess_number_obj = GuessNumber()
    guess_number_obj.secret_number = secret_number

    request.session['guess_number_obj'] = guess_number_obj

    context = {'secret_number': secret_number}

    return HttpResponse(template.render(context, request))


def check_guess(request):
    template = loader.get_template('fun/guessnumber.html')
    helpView = HelpView()
    user_input = request.POST["Enter Your Guess"]

    guess_number_obj = request.session['guess_number_obj']

    if user_input.isdigit():
        number = int(user_input)
        guess_number_obj.guessed_number = number
        guess_number_obj.guesses.append(number)

        if guess_number_obj.guessed_number < guess_number_obj.secret_number:
            guess_number_obj.comparison = 'lesser'
        elif guess_number_obj.guessed_number > guess_number_obj.secret_number:
            guess_number_obj.comparison = 'greater'
        else:
            guess_number_obj.comparison = 'equal'
            guess_number_obj.addResult(0)
            helpView.getUserGuessesAndCounts(guess_number_obj.getStats())

        request.session['guess_number_obj'] = guess_number_obj
        context = {'guess_number': guess_number_obj, 'guess_count': len(guess_number_obj.guesses),
                   'user_guesses': helpView.user_guesses, 'counts': helpView.counts}
    else:
        error_message = 'Please enter a number'
        context = {'error_message': error_message, 'guess_count': len(guess_number_obj.guesses)}

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
        context = {'welcome_message': welcome_message, 'numberdle_obj': numberdle_obj,
                   'user_guesses': helpView.user_guesses, 'counts': helpView.counts}
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


def spelling_bee(request):
    template = loader.get_template('fun/spelling.html')

    welcome_message = 'Spelling Bee!'

    tts = gTTS(text=welcome_message, lang='en-us')
    tts.save("voice.mp3")

    context = {'welcome_message': welcome_message, 'tts': tts}
    print(context)

    return HttpResponse(template.render(context, request))
