import random

# Create your views here.
from django.http import HttpResponse
from django.template import loader

from fun.contentGeneratorAI import generateSentence
from fun.helpView import HelpView
from fun.models.countriesConnection import CountriesConnection
from fun.models.feedback import Feedback
from fun.models.guessNumber import GuessNumber
from fun.models.models import CrazyLibs
from fun.models.numberdle import Numberdle
from fun.models.spellingBee import SpellingBee
from fun.models.usage import Usage
from myFirstDjangoSite.settings import env


# from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


def index(request):
    template = loader.get_template('fun/index.html')
    welcome_message = 'My Fun Hub!'
    print(request.META)

    try:
        usage = Usage()
        usage.saveUsage(request.META['REMOTE_ADDR'], request.META['HTTP_HOST'], request.META['HTTP_USER_AGENT'],
                        request.META['HTTP_X_REAL_IP'], request.META['HTTP_X_FORWARDED_FOR'])
    except:
        print('localhost')

    context = {'welcome_message': welcome_message}

    try:
        feedback = request.POST["Enter Feedback"]
        email = request.POST["Enter Email"]
        print('feedback = ' + feedback + ' email = ' + email)
        Feedback().addFeedback(0, feedback, email)
        context['feedback'] = 'success'
    except:
        print('direct landing')

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
    try:
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
    except:
        return guess_number(request)


def crazy_libs(request):
    template = loader.get_template('fun/crazylibs.html')

    crazyLibsObj = CrazyLibs()
    crazyLibsObj.tokenize()

    # text = 'Thats true. Fans usually only boo players or teams that they are familiar with or have a history with. ' \
    #        'Setting session crazyLibsObj. Fans dont boo nobodies.'

    # wordcloud = WordCloud().generate(text)

    context = {'story': crazyLibsObj.original_story(), 'nouns': crazyLibsObj.nouns,
               'verbs': crazyLibsObj.verbs, 'adjectives': crazyLibsObj.adjectives}

    request.session['crazyLibsObj'] = crazyLibsObj
    print("setting session crazyLibsObj: " + str(crazyLibsObj.__str__()))
    return HttpResponse(template.render(context, request))


def generate_crazy_libs(request):
    template = loader.get_template('fun/crazylibs.html')
    crazyLibsObj = request.session['crazyLibsObj']
    print("received session crazyLibsObj: " + str(crazyLibsObj.__str__()))

    for noun in crazyLibsObj.nouns:
        input_noun = str(request.POST.get("input_noun_" + noun))
        print("input_noun_" + noun + ": " + input_noun)
        if input_noun != '' and len(input_noun) > 2:
            crazyLibsObj.make_crazy(noun, input_noun)

    for verb in crazyLibsObj.verbs:
        input_verb = str(request.POST.get("input_verb_" + verb))
        print("input_verb_" + verb + ": " + input_verb)
        if input_verb != '' and len(input_verb) > 2:
            crazyLibsObj.make_crazy(verb, input_verb)

    for adjective in crazyLibsObj.adjectives:
        input_adjective = str(request.POST.get("input_adjective_" + adjective))
        print("input_adjective_" + adjective + ": " + input_adjective)
        if input_adjective != '' and len(input_adjective) > 2:
            crazyLibsObj.make_crazy(adjective, input_adjective)

    print("The final crazy story is" + crazyLibsObj.crazy_story)
    request.session['crazyLibsObj'] = crazyLibsObj

    print("setting session crazyLibsObj: " + str(crazyLibsObj.__str__()))

    crazyLibsObj.addResult(0)

    crazyLibsObj.getStats()

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
    countries_connection_obj = None

    try:
        countries_connection_obj = request.session['countries_connection_obj']
    except:
        print('countries_connection_obj not present')

    if countries_connection_obj:
        countries_connection_obj.addResult(0)
    else:
        print(' direct countries connection')

    countries_connection_obj = CountriesConnection()
    request.session['countries_connection_obj'] = countries_connection_obj

    helpView = HelpView()
    helpView.getUserScoresAndCounts(countries_connection_obj.getStats())

    request.session['user_scores'] = helpView.user_scores
    request.session['counts'] = helpView.counts

    context = {'welcome_message': welcome_message, 'countries_connection_obj': countries_connection_obj,
               'user_scores': request.session['user_scores'], 'counts': request.session['counts']}
    print(context)

    return HttpResponse(template.render(context, request))


def connect_country(request):
    try:
        template = loader.get_template('fun/countriesconnection.html')

        player_input = str(request.POST.get("Enter Country")).strip()

        countries_connection_obj = request.session['countries_connection_obj']

        result = countries_connection_obj.connect_country(player_input)

        request.session['countries_connection_obj'] = countries_connection_obj

        context = {'countries_connection_obj': countries_connection_obj, 'result': result,
                   'user_scores': request.session['user_scores'], 'counts': request.session['counts']}
        print(context)

        return HttpResponse(template.render(context, request))
    except:
        return countries_connection(request)


def spelling_bee(request):
    template = loader.get_template('fun/spelling.html')

    welcome_message = 'Spelling Bee!'

    language = 'en-us'

    spelling_bee_obj = SpellingBee()

    word = spelling_bee_obj.current_word
    sentence = generateSentence(word)

    print('word: ' + word + ' - sentence: ' + sentence)

    # words = word_list['word']

    words = "['word1', 'word2', 'word3', 'word4', 'word5', 'word6', 'word7', 'word8', 'word9', 'word10', 'word11', " \
            "'word12', 'word13', 'word14', 'word15', 'word16', 'word17', 'word18', 'word19', 'word20', 'word21', " \
            "'word22', 'word23', 'word24']"

    # word_correct = word_list['count_right']
    # word_incorrect = word_list['count_wrong']

    word_correct = "[10, 25, 50, 10, 25, 50, 10, 25, 50, 10, 25, 50, 10, 25, 50, 10, 25, 50, 10, 25, 50, 10, 25, 50]"

    word_incorrect = "[-50, -25, -10, -50, -25, -10, -50, -25, -10, -50, -25, -10, -50, -25, -10, -50, -25, -10, -50, " \
                     "-25, -10, -50, -25, -10]"

    dates = "['1/1/2023', '1/2/2013', '1/3/2023', '1/4/2023', '1/5/2023', '1/6/2023', '1/7/2023']"

    date_correct = "[1, 10, 20, 25, 45, 50, 50]"

    date_incorrect = "[49, 40, 30, 25, 5, 0, 0]"
    context = {'welcome_message': welcome_message, 'words': words, 'word_correct': word_correct,
               'word_incorrect': word_incorrect, 'dates': dates, 'date_correct': date_correct,
               'date_incorrect': date_incorrect, 'word': word, 'sentence': sentence, 'language': language}

    print(context)

    request.session['spelling_bee_obj'] = spelling_bee_obj

    return HttpResponse(template.render(context, request))


def spell_check(request):
    try:
        template = loader.get_template('fun/spelling.html')

        user_input = request.POST["Enter Spelling"]

        language = 'en-us'

        spelling_bee_obj = request.session['spelling_bee_obj']

        result = spelling_bee_obj.spellCheck(user_input)

        if result:
            word = spelling_bee_obj.getNewWord()
        else:
            word = spelling_bee_obj.current_word

        sentence = generateSentence(word)

        request.session['spelling_bee_obj'] = spelling_bee_obj

        context = {'word': word, 'sentence': sentence, 'language': language, 'result': result,
                   'tries': spelling_bee_obj.tries, 'correct': spelling_bee_obj.correct,
                   'incorrect': spelling_bee_obj.incorrect, 'previous_input': user_input}

        print(context)

        return HttpResponse(template.render(context, request))
    except:
        return spelling_bee(request)


def spell_new(request):
    template = loader.get_template('fun/spelling.html')

    language = 'en-us'

    spelling_bee_obj = request.session['spelling_bee_obj']

    result = 'new'
    old_word = ''

    if not spelling_bee_obj:
        spelling_bee_obj = SpellingBee()
    else:
        old_word = spelling_bee_obj.current_word
        spelling_bee_obj.getNewWord()

    word = spelling_bee_obj.current_word
    sentence = generateSentence(word)

    request.session['spelling_bee_obj'] = spelling_bee_obj

    print('word: ' + word + ' - sentence: ' + sentence)

    context = {'word': word, 'sentence': sentence, 'language': language, 'result': result, 'old_word': old_word,
               'tries': spelling_bee_obj.tries, 'correct': spelling_bee_obj.correct,
               'incorrect': spelling_bee_obj.incorrect}

    print(context)

    return HttpResponse(template.render(context, request))


def feedback(request):
    template = loader.get_template('fun/feedback.html')
    feedback_message = 'Feedback!'

    context = {'feedback_message': feedback_message}

    print(context)
    return HttpResponse(template.render(context, request))

def stocks(request):
    template = loader.get_template('fun/stocks.html')
    feedback_message = 'Stocks!'

    context = {'feedback_message': feedback_message}

    print(context)
    return HttpResponse(template.render(context, request))
