import random

from django.contrib.auth.models import AnonymousUser
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.utils.datastructures import MultiValueDictKeyError

from fun.contentGeneratorAI import generateSentence
from fun.helpView import HelpView
from fun.models.countriesConnection import CountriesConnection
from fun.models.feedback import Feedback
from fun.models.newsletter import Newsletter
from fun.models.guessNumber import GuessNumber
from fun.models.models import CrazyLibs
from fun.models.numberdle import Numberdle
from fun.models.spellingBee import SpellingBee
from fun.models.stocks import Stocks
from fun.models.usage import Usage
from fun.models.puzzle import Puzzle
from fun.paymentGateway import PymentGateway
from myFirstDjangoSite.settings import env


# from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


def index(request):
    template = loader.get_template("fun/index.html")
    welcome_message = "My Fun Hub!"
    print(request.META)

    try:
        usage = Usage()
<<<<<<< HEAD
        usage.saveUsage(0, request.META['REMOTE_ADDR'], request.META['HTTP_HOST'], request.META['HTTP_USER_AGENT'],
                        request.META['HTTP_X_REAL_IP'], request.META['HTTP_X_FORWARDED_FOR'])
    except Exception as e:
        print('exception when saving usage: ' + str(e))

    context = {'welcome_message': welcome_message}
=======
        usage.saveUsage(
            0,
            request.META["REMOTE_ADDR"],
            request.META["HTTP_HOST"],
            request.META["HTTP_USER_AGENT"],
            request.META["HTTP_X_REAL_IP"],
            request.META["HTTP_X_FORWARDED_FOR"],
        )
    except Exception as e:
        print("exception when saving usage: " + str(e))

    context = {"welcome_message": welcome_message}
>>>>>>> a9be7de (commit and push everything)

    try:
        feedback = request.POST["Enter Feedback"]
        email = request.POST["Enter Email"]
<<<<<<< HEAD
        print('feedback = ' + feedback + ' email = ' + email)
        Feedback().addFeedback(0, feedback, email)
        context['feedback'] = 'success'
=======
        print("feedback = " + feedback + " email = " + email)
        Feedback().addFeedback(0, feedback, email)
        context["feedback"] = "success"
>>>>>>> a9be7de (commit and push everything)
    except MultiValueDictKeyError as ex:
        try:
            print(type(ex).__name__)
            email = request.POST["Enter Email"]
<<<<<<< HEAD
            print('signup email: ' + email)
            Newsletter().addNewsletterSignUp(email)
            context['signup'] = 'success'
        except:
            print('direct landing')

    print(context)
    print('LOVE is ' + str(env('LOVE')))

    if str(request.user) == 'AnonymousUser':
        print('user is not logged in')
    else:
        print('user = ' + str(request.user))

    return HttpResponse(template.render(context, request))

def guess_number(request):
    template = loader.get_template('fun/guessnumber.html')
=======
            print("signup email: " + email)
            Newsletter().addNewsletterSignUp(email)
            context["signup"] = "success"
        except:
            print("direct landing")

    print(context)
    print("LOVE is " + str(env("LOVE")))

    if str(request.user) == "AnonymousUser":
        print("user is not logged in")
    else:
        print("user = " + str(request.user))

    return HttpResponse(template.render(context, request))


def guess_number(request):
    template = loader.get_template("fun/guessnumber.html")
>>>>>>> a9be7de (commit and push everything)
    secret_number = random.randint(1, 100)

    guess_number_obj = GuessNumber()
    guess_number_obj.secret_number = secret_number

<<<<<<< HEAD
    request.session['guess_number_obj'] = guess_number_obj

    context = {'secret_number': secret_number}
=======
    request.session["guess_number_obj"] = guess_number_obj

    context = {"secret_number": secret_number}
>>>>>>> a9be7de (commit and push everything)

    return HttpResponse(template.render(context, request))


def check_guess(request):
    try:
<<<<<<< HEAD
        template = loader.get_template('fun/guessnumber.html')
        helpView = HelpView()
        user_input = request.POST["Enter Your Guess"]

        guess_number_obj = request.session['guess_number_obj']
=======
        template = loader.get_template("fun/guessnumber.html")
        helpView = HelpView()
        user_input = request.POST["Enter Your Guess"]

        guess_number_obj = request.session["guess_number_obj"]
>>>>>>> a9be7de (commit and push everything)

        if user_input.isdigit():
            number = int(user_input)
            guess_number_obj.guessed_number = number
            guess_number_obj.guesses.append(number)

            if guess_number_obj.guessed_number < guess_number_obj.secret_number:
<<<<<<< HEAD
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
=======
                guess_number_obj.comparison = "lesser"
            elif guess_number_obj.guessed_number > guess_number_obj.secret_number:
                guess_number_obj.comparison = "greater"
            else:
                guess_number_obj.comparison = "equal"
                guess_number_obj.addResult(0)
                helpView.getUserGuessesAndCounts(guess_number_obj.getStats())

            request.session["guess_number_obj"] = guess_number_obj
            context = {
                "guess_number": guess_number_obj,
                "guess_count": len(guess_number_obj.guesses),
                "user_guesses": helpView.user_guesses,
                "counts": helpView.counts,
            }
        else:
            error_message = "Please enter a number"
            context = {
                "error_message": error_message,
                "guess_count": len(guess_number_obj.guesses),
            }
>>>>>>> a9be7de (commit and push everything)

        return HttpResponse(template.render(context, request))
    except:
        return guess_number(request)


def crazy_libs(request):
<<<<<<< HEAD
    template = loader.get_template('fun/crazylibs.html')
=======
    template = loader.get_template("fun/crazylibs.html")
>>>>>>> a9be7de (commit and push everything)

    crazyLibsObj = CrazyLibs()
    crazyLibsObj.tokenize()

    # text = 'Thats true. Fans usually only boo players or teams that they are familiar with or have a history with. ' \
    #        'Setting session crazyLibsObj. Fans dont boo nobodies.'

    # wordcloud = WordCloud().generate(text)

<<<<<<< HEAD
    context = {'story': crazyLibsObj.original_story(), 'nouns': crazyLibsObj.nouns,
               'verbs': crazyLibsObj.verbs, 'adjectives': crazyLibsObj.adjectives}

    request.session['crazyLibsObj'] = crazyLibsObj
=======
    context = {
        "story": crazyLibsObj.original_story(),
        "nouns": crazyLibsObj.nouns,
        "verbs": crazyLibsObj.verbs,
        "adjectives": crazyLibsObj.adjectives,
    }

    request.session["crazyLibsObj"] = crazyLibsObj
>>>>>>> a9be7de (commit and push everything)
    print("setting session crazyLibsObj: " + str(crazyLibsObj.__str__()))
    return HttpResponse(template.render(context, request))


def generate_crazy_libs(request):
<<<<<<< HEAD
    template = loader.get_template('fun/crazylibs.html')
    crazyLibsObj = request.session['crazyLibsObj']
=======
    template = loader.get_template("fun/crazylibs.html")
    crazyLibsObj = request.session["crazyLibsObj"]
>>>>>>> a9be7de (commit and push everything)
    print("received session crazyLibsObj: " + str(crazyLibsObj.__str__()))

    for noun in crazyLibsObj.nouns:
        input_noun = str(request.POST.get("input_noun_" + noun))
        print("input_noun_" + noun + ": " + input_noun)
<<<<<<< HEAD
        if input_noun != '' and len(input_noun) > 2:
=======
        if input_noun != "" and len(input_noun) > 2:
>>>>>>> a9be7de (commit and push everything)
            crazyLibsObj.make_crazy(noun, input_noun)

    for verb in crazyLibsObj.verbs:
        input_verb = str(request.POST.get("input_verb_" + verb))
        print("input_verb_" + verb + ": " + input_verb)
<<<<<<< HEAD
        if input_verb != '' and len(input_verb) > 2:
=======
        if input_verb != "" and len(input_verb) > 2:
>>>>>>> a9be7de (commit and push everything)
            crazyLibsObj.make_crazy(verb, input_verb)

    for adjective in crazyLibsObj.adjectives:
        input_adjective = str(request.POST.get("input_adjective_" + adjective))
        print("input_adjective_" + adjective + ": " + input_adjective)
<<<<<<< HEAD
        if input_adjective != '' and len(input_adjective) > 2:
            crazyLibsObj.make_crazy(adjective, input_adjective)

    print("The final crazy story is" + crazyLibsObj.crazy_story)
    request.session['crazyLibsObj'] = crazyLibsObj
=======
        if input_adjective != "" and len(input_adjective) > 2:
            crazyLibsObj.make_crazy(adjective, input_adjective)

    print("The final crazy story is" + crazyLibsObj.crazy_story)
    request.session["crazyLibsObj"] = crazyLibsObj
>>>>>>> a9be7de (commit and push everything)

    print("setting session crazyLibsObj: " + str(crazyLibsObj.__str__()))

    crazyLibsObj.addResult(0)

    crazyLibsObj.getStats()

<<<<<<< HEAD
    context = {'crazyLibsObj': crazyLibsObj}
=======
    context = {"crazyLibsObj": crazyLibsObj}
>>>>>>> a9be7de (commit and push everything)

    return HttpResponse(template.render(context, request))


def numberdle(request):
<<<<<<< HEAD
    template = loader.get_template('fun/numberdle.html')
    welcome_message = 'Numberdle!'

    numberdle_obj = Numberdle()
    request.session['numberdle_obj'] = numberdle_obj
    context = {'welcome_message': welcome_message, 'numberdle_obj': numberdle_obj}
=======
    template = loader.get_template("fun/numberdle.html")
    welcome_message = "Numberdle!"

    numberdle_obj = Numberdle()
    request.session["numberdle_obj"] = numberdle_obj
    context = {"welcome_message": welcome_message, "numberdle_obj": numberdle_obj}
>>>>>>> a9be7de (commit and push everything)
    print(numberdle_obj.secret_numbers)
    print(context)

    return HttpResponse(template.render(context, request))


def check_numberdle(request):
<<<<<<< HEAD
    template = loader.get_template('fun/numberdle.html')
    welcome_message = 'Numberdle!'
    numberdle_obj = request.session['numberdle_obj']
=======
    template = loader.get_template("fun/numberdle.html")
    welcome_message = "Numberdle!"
    numberdle_obj = request.session["numberdle_obj"]
>>>>>>> a9be7de (commit and push everything)
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

<<<<<<< HEAD
        request.session['numberdle_obj'] = numberdle_obj
        context = {'welcome_message': welcome_message, 'numberdle_obj': numberdle_obj,
                   'user_guesses': helpView.user_guesses, 'counts': helpView.counts}
        print(context)
    else:
        error_message = 'Please enter a number'
        context = {'error_message': error_message, 'welcome_message': welcome_message, 'numberdle_obj': numberdle_obj}
=======
        request.session["numberdle_obj"] = numberdle_obj
        context = {
            "welcome_message": welcome_message,
            "numberdle_obj": numberdle_obj,
            "user_guesses": helpView.user_guesses,
            "counts": helpView.counts,
        }
        print(context)
    else:
        error_message = "Please enter a number"
        context = {
            "error_message": error_message,
            "welcome_message": welcome_message,
            "numberdle_obj": numberdle_obj,
        }
>>>>>>> a9be7de (commit and push everything)

    return HttpResponse(template.render(context, request))


def countries_connection(request):
<<<<<<< HEAD
    template = loader.get_template('fun/countriesconnection.html')
    welcome_message = 'Countries Connection!'
    countries_connection_obj = None

    try:
        countries_connection_obj = request.session['countries_connection_obj']
    except:
        print('countries_connection_obj not present')
=======
    template = loader.get_template("fun/countriesconnection.html")
    welcome_message = "Countries Connection!"
    countries_connection_obj = None

    try:
        countries_connection_obj = request.session["countries_connection_obj"]
    except:
        print("countries_connection_obj not present")
>>>>>>> a9be7de (commit and push everything)

    if countries_connection_obj:
        countries_connection_obj.addResult(0)
    else:
<<<<<<< HEAD
        print(' direct countries connection')

    countries_connection_obj = CountriesConnection()
    request.session['countries_connection_obj'] = countries_connection_obj
=======
        print(" direct countries connection")

    countries_connection_obj = CountriesConnection()
    request.session["countries_connection_obj"] = countries_connection_obj
>>>>>>> a9be7de (commit and push everything)

    helpView = HelpView()
    helpView.getUserScoresAndCounts(countries_connection_obj.getStats())

<<<<<<< HEAD
    request.session['user_scores'] = helpView.user_scores
    request.session['counts'] = helpView.counts

    context = {'welcome_message': welcome_message, 'countries_connection_obj': countries_connection_obj,
               'user_scores': request.session['user_scores'], 'counts': request.session['counts']}
=======
    request.session["user_scores"] = helpView.user_scores
    request.session["counts"] = helpView.counts

    context = {
        "welcome_message": welcome_message,
        "countries_connection_obj": countries_connection_obj,
        "user_scores": request.session["user_scores"],
        "counts": request.session["counts"],
    }
>>>>>>> a9be7de (commit and push everything)
    print(context)

    return HttpResponse(template.render(context, request))


def connect_country(request):
    try:
<<<<<<< HEAD
        template = loader.get_template('fun/countriesconnection.html')

        player_input = str(request.POST.get("Enter Country")).strip()

        countries_connection_obj = request.session['countries_connection_obj']

        result = countries_connection_obj.connect_country(player_input)

        request.session['countries_connection_obj'] = countries_connection_obj

        context = {'countries_connection_obj': countries_connection_obj, 'result': result,
                   'user_scores': request.session['user_scores'], 'counts': request.session['counts']}
=======
        template = loader.get_template("fun/countriesconnection.html")

        player_input = str(request.POST.get("Enter Country")).strip()

        countries_connection_obj = request.session["countries_connection_obj"]

        result = countries_connection_obj.connect_country(player_input)

        request.session["countries_connection_obj"] = countries_connection_obj

        context = {
            "countries_connection_obj": countries_connection_obj,
            "result": result,
            "user_scores": request.session["user_scores"],
            "counts": request.session["counts"],
        }
>>>>>>> a9be7de (commit and push everything)
        print(context)

        return HttpResponse(template.render(context, request))
    except:
        return countries_connection(request)


def spelling_bee(request):
<<<<<<< HEAD
    template = loader.get_template('fun/spelling.html')

    bee_user = request.user

    print('username = ' + str(bee_user) + ', user id = ' + str(bee_user.id))

    welcome_message = bee_user.username + ', welcome to Spelling Bee!'

    language = 'en-us'
=======
    template = loader.get_template("fun/spelling.html")

    bee_user = request.user

    print("username = " + str(bee_user) + ", user id = " + str(bee_user.id))

    welcome_message = bee_user.username + ", welcome to Spelling Bee!"

    language = "en-us"
>>>>>>> a9be7de (commit and push everything)

    spelling_bee_obj = SpellingBee()

    word = spelling_bee_obj.current_word
    sentence = generateSentence(word)

<<<<<<< HEAD
    print('word: ' + word + ' - sentence: ' + sentence)

    # words = word_list['word']

    words = "['word1', 'word2', 'word3', 'word4', 'word5', 'word6', 'word7', 'word8', 'word9', 'word10', 'word11', " \
            "'word12', 'word13', 'word14', 'word15', 'word16', 'word17', 'word18', 'word19', 'word20', 'word21', " \
            "'word22', 'word23', 'word24']"
=======
    print("word: " + word + " - sentence: " + sentence)

    # words = word_list['word']

    words = (
        "['word1', 'word2', 'word3', 'word4', 'word5', 'word6', 'word7', 'word8', 'word9', 'word10', 'word11', "
        "'word12', 'word13', 'word14', 'word15', 'word16', 'word17', 'word18', 'word19', 'word20', 'word21', "
        "'word22', 'word23', 'word24']"
    )
>>>>>>> a9be7de (commit and push everything)

    # word_correct = word_list['count_right']
    # word_incorrect = word_list['count_wrong']

    word_correct = "[10, 25, 50, 10, 25, 50, 10, 25, 50, 10, 25, 50, 10, 25, 50, 10, 25, 50, 10, 25, 50, 10, 25, 50]"

<<<<<<< HEAD
    word_incorrect = "[-50, -25, -10, -50, -25, -10, -50, -25, -10, -50, -25, -10, -50, -25, -10, -50, -25, -10, -50, " \
                     "-25, -10, -50, -25, -10]"
=======
    word_incorrect = (
        "[-50, -25, -10, -50, -25, -10, -50, -25, -10, -50, -25, -10, -50, -25, -10, -50, -25, -10, -50, "
        "-25, -10, -50, -25, -10]"
    )
>>>>>>> a9be7de (commit and push everything)

    dates = "['1/1/2023', '1/2/2013', '1/3/2023', '1/4/2023', '1/5/2023', '1/6/2023', '1/7/2023']"

    date_correct = "[1, 10, 20, 25, 45, 50, 50]"

    date_incorrect = "[49, 40, 30, 25, 5, 0, 0]"
<<<<<<< HEAD
    context = {'welcome_message': welcome_message, 'words': words, 'word_correct': word_correct,
               'word_incorrect': word_incorrect, 'dates': dates, 'date_correct': date_correct,
               'date_incorrect': date_incorrect, 'word': word, 'sentence': sentence, 'language': language}

    print(context)

    request.session['spelling_bee_obj'] = spelling_bee_obj
=======
    context = {
        "welcome_message": welcome_message,
        "words": words,
        "word_correct": word_correct,
        "word_incorrect": word_incorrect,
        "dates": dates,
        "date_correct": date_correct,
        "date_incorrect": date_incorrect,
        "word": word,
        "sentence": sentence,
        "language": language,
    }

    print(context)

    request.session["spelling_bee_obj"] = spelling_bee_obj
>>>>>>> a9be7de (commit and push everything)

    return HttpResponse(template.render(context, request))


def spell_check(request):
    try:
<<<<<<< HEAD
        template = loader.get_template('fun/spelling.html')

        user_input = request.POST["Enter Spelling"]

        language = 'en-us'

        spelling_bee_obj = request.session['spelling_bee_obj']
=======
        template = loader.get_template("fun/spelling.html")

        user_input = request.POST["Enter Spelling"]

        language = "en-us"

        spelling_bee_obj = request.session["spelling_bee_obj"]
>>>>>>> a9be7de (commit and push everything)

        result = spelling_bee_obj.spellCheck(user_input)

        if result:
            word = spelling_bee_obj.getNewWord()
        else:
            word = spelling_bee_obj.current_word

        sentence = generateSentence(word)

<<<<<<< HEAD
        request.session['spelling_bee_obj'] = spelling_bee_obj

        context = {'word': word, 'sentence': sentence, 'language': language, 'result': result,
                   'tries': spelling_bee_obj.tries, 'correct': spelling_bee_obj.correct,
                   'incorrect': spelling_bee_obj.incorrect, 'previous_input': user_input}
=======
        request.session["spelling_bee_obj"] = spelling_bee_obj

        context = {
            "word": word,
            "sentence": sentence,
            "language": language,
            "result": result,
            "tries": spelling_bee_obj.tries,
            "correct": spelling_bee_obj.correct,
            "incorrect": spelling_bee_obj.incorrect,
            "previous_input": user_input,
        }
>>>>>>> a9be7de (commit and push everything)

        print(context)

        return HttpResponse(template.render(context, request))
    except:
        return spelling_bee(request)


def spell_new(request):
<<<<<<< HEAD
    template = loader.get_template('fun/spelling.html')

    language = 'en-us'

    spelling_bee_obj = request.session['spelling_bee_obj']

    result = 'new'
    old_word = ''
=======
    template = loader.get_template("fun/spelling.html")

    language = "en-us"

    spelling_bee_obj = request.session["spelling_bee_obj"]

    result = "new"
    old_word = ""
>>>>>>> a9be7de (commit and push everything)

    if not spelling_bee_obj:
        spelling_bee_obj = SpellingBee()
    else:
        old_word = spelling_bee_obj.current_word
        spelling_bee_obj.getNewWord()

    word = spelling_bee_obj.current_word
    sentence = generateSentence(word)

<<<<<<< HEAD
    request.session['spelling_bee_obj'] = spelling_bee_obj

    print('word: ' + word + ' - sentence: ' + sentence)

    context = {'word': word, 'sentence': sentence, 'language': language, 'result': result, 'old_word': old_word,
               'tries': spelling_bee_obj.tries, 'correct': spelling_bee_obj.correct,
               'incorrect': spelling_bee_obj.incorrect}
=======
    request.session["spelling_bee_obj"] = spelling_bee_obj

    print("word: " + word + " - sentence: " + sentence)

    context = {
        "word": word,
        "sentence": sentence,
        "language": language,
        "result": result,
        "old_word": old_word,
        "tries": spelling_bee_obj.tries,
        "correct": spelling_bee_obj.correct,
        "incorrect": spelling_bee_obj.incorrect,
    }
>>>>>>> a9be7de (commit and push everything)

    print(context)

    return HttpResponse(template.render(context, request))


def feedback(request):
<<<<<<< HEAD
    template = loader.get_template('fun/feedback.html')
    feedback_message = 'Feedback!'

    context = {'feedback_message': feedback_message}
=======
    template = loader.get_template("fun/feedback.html")
    feedback_message = "Feedback!"

    context = {"feedback_message": feedback_message}
>>>>>>> a9be7de (commit and push everything)

    print(context)
    return HttpResponse(template.render(context, request))


def stocks(request):
<<<<<<< HEAD
    template = loader.get_template('fun/stocks.html')
    welcome = 'Stocks!'
=======
    template = loader.get_template("fun/stocks.html")
    welcome = "Stocks!"
>>>>>>> a9be7de (commit and push everything)

    stocks = Stocks()
    superStars = stocks.getSuperStars()

<<<<<<< HEAD
    dataSuperStars = "{                           " \
           "   labels: labels1,          " \
           "   datasets: [               "

    for stock in superStars:
        dataSuperStars = dataSuperStars + "     {                       " \
                      "       label: '" + str(stock.ticker) + '\',' \
                      "       data:" + str(stock.performance) + \
               "     },                      " \

    dataSuperStars = dataSuperStars + "   ]                         " \
                  " }; "

    risingStars = stocks.getRisingStars()

    dataRisingStars = "{                           " \
                     "   labels: labels2,          " \
                     "   datasets: [               "

    for stock in risingStars:
        dataRisingStars = dataRisingStars + "     {                       " \
                        "       label: '" + str(stock.ticker) + '\',' \
                        "       data:" + str(stock.performance) + \
                        "     },                      " \

    dataRisingStars = dataRisingStars + "   ]                         " \
                    " }; "

    spyWinners = stocks.getSPYWinners()

    dataSPYWinners = "{                           " \
                     "   labels: labels3,          " \
                     "   datasets: [               "

    for stock in spyWinners:
        dataSPYWinners = dataSPYWinners + "     {                       " \
                                          "       label: '" + str(stock.ticker) + '\',' \
                                          "       data:" + str(stock.performance) + \
                                          "     },                      " \

    dataSPYWinners = dataSPYWinners + "   ]                         " \
                " }; "

    context = {'welcome': welcome, 'dataSuperStars': dataSuperStars, 'labelsSuperStars': superStars[0].times,
               'dataRisingStars': dataRisingStars, 'labelsRisingStars': risingStars[0].times,
               'dataSPYWinners': dataSPYWinners, 'labelsSPYWinners': spyWinners[0].times}
=======
    dataSuperStars = (
        "{                           "
        "   labels: labels1,          "
        "   datasets: [               "
    )

    for stock in superStars:
        dataSuperStars = (
            dataSuperStars + "     {                       "
            "       label: '" + str(stock.ticker) + "',"
            "       data:" + str(stock.performance) + "     },                      "
        )
    dataSuperStars = dataSuperStars + "   ]                         " " }; "

    risingStars = stocks.getRisingStars()

    dataRisingStars = (
        "{                           "
        "   labels: labels2,          "
        "   datasets: [               "
    )

    for stock in risingStars:
        dataRisingStars = (
            dataRisingStars + "     {                       "
            "       label: '" + str(stock.ticker) + "',"
            "       data:" + str(stock.performance) + "     },                      "
        )
    dataRisingStars = dataRisingStars + "   ]                         " " }; "

    spyWinners = stocks.getSPYWinners()

    dataSPYWinners = (
        "{                           "
        "   labels: labels3,          "
        "   datasets: [               "
    )

    for stock in spyWinners:
        dataSPYWinners = (
            dataSPYWinners + "     {                       "
            "       label: '" + str(stock.ticker) + "',"
            "       data:" + str(stock.performance) + "     },                      "
        )
    dataSPYWinners = dataSPYWinners + "   ]                         " " }; "

    context = {
        "welcome": welcome,
        "dataSuperStars": dataSuperStars,
        "labelsSuperStars": superStars[0].times,
        "dataRisingStars": dataRisingStars,
        "labelsRisingStars": risingStars[0].times,
        "dataSPYWinners": dataSPYWinners,
        "labelsSPYWinners": spyWinners[0].times,
    }
>>>>>>> a9be7de (commit and push everything)

    print(context)
    return HttpResponse(template.render(context, request))


def sorting_hat(request):
<<<<<<< HEAD
    template = loader.get_template('fun/sortinghat.html')
    welcome = 'Sorting Hat!'

    context = {'welcome': welcome}
=======
    template = loader.get_template("fun/sortinghat.html")
    welcome = "Sorting Hat!"

    context = {"welcome": welcome}
>>>>>>> a9be7de (commit and push everything)

    print(context)
    return HttpResponse(template.render(context, request))


def sorting_hat_admin(request):
<<<<<<< HEAD
    template = loader.get_template('fun/sortinghatadmin.html')
    welcome = 'Sorting Hat Admin!'

    context = {'welcome': welcome}
=======
    template = loader.get_template("fun/sortinghatadmin.html")
    welcome = "Sorting Hat Admin!"

    context = {"welcome": welcome}
>>>>>>> a9be7de (commit and push everything)

    print(context)
    return HttpResponse(template.render(context, request))

<<<<<<< HEAD
def puzzles(request):

    if str(request.user) == 'AnonymousUser':
        print('user is not logged in')
        return HttpResponseRedirect('../accounts/login/?next=' + request.path)

    template = loader.get_template('fun/puzzles.html')
    welcome = 'It\'s a Puzzle Party!'
=======

def puzzles(request):
    if str(request.user) == "AnonymousUser":
        print("user is not logged in")
        return HttpResponseRedirect("../accounts/login/?next=" + request.path)

    template = loader.get_template("fun/puzzles.html")
    welcome = "It's a Puzzle Party!"
>>>>>>> a9be7de (commit and push everything)

    puzzle = Puzzle()

    puzzle.getPuzzle()

<<<<<<< HEAD
    request.session['puzzle_obj'] = puzzle

    context = {'welcome': welcome, 'puzzle': puzzle}
=======
    request.session["puzzle_obj"] = puzzle

    context = {"welcome": welcome, "puzzle": puzzle}
>>>>>>> a9be7de (commit and push everything)

    print(context)
    return HttpResponse(template.render(context, request))

<<<<<<< HEAD
def check_puzzle_answer(request):
    try:
        template = loader.get_template('fun/puzzles.html')
        welcome = 'It\'s a Puzzle Party!'

        player_answer = str(request.POST.get("Answer")).strip()

        puzzle = request.session['puzzle_obj']
=======

def check_puzzle_answer(request):
    try:
        template = loader.get_template("fun/puzzles.html")
        welcome = "It's a Puzzle Party!"

        player_answer = str(request.POST.get("Answer")).strip()

        puzzle = request.session["puzzle_obj"]
>>>>>>> a9be7de (commit and push everything)

        puzzle.answer = player_answer

        puzzle.validateAnswer()

        print(puzzle)

<<<<<<< HEAD
        validation = puzzle.validation + ' <br> ' + puzzle.solution

        puzzle.getPuzzle()

        request.session['puzzle_obj'] = puzzle

        context = {'welcome': welcome, 'puzzle': puzzle, 'validation': validation}
=======
        validation = puzzle.validation + " <br> " + puzzle.solution

        puzzle.getPuzzle()

        request.session["puzzle_obj"] = puzzle

        context = {"welcome": welcome, "puzzle": puzzle, "validation": validation}
>>>>>>> a9be7de (commit and push everything)

        print(context)
        return HttpResponse(template.render(context, request))

    except:
        return puzzles(request)

<<<<<<< HEAD
def signup(request):
    try:
        template = loader.get_template('fun/signup.html')
        welcome = 'Sign Up!'
        context = {'welcome': welcome}

        print('signup called')
        print(request.session.items())
        for key, value in request.session.items():
            print('{} => {}'.format(key, value))
=======

def signup(request):
    try:
        template = loader.get_template("fun/signup.html")
        welcome = "Sign Up!"
        context = {"welcome": welcome}

        print("signup called")
        print(request.session.items())
        for key, value in request.session.items():
            print("{} => {}".format(key, value))
>>>>>>> a9be7de (commit and push everything)

        print(context)
        return HttpResponse(template.render(context, request))

    except Exception as ex:
        print(ex.__str__())
        return index(request)

<<<<<<< HEAD
def process_payment(request):
    try:
        paymentGateway = PymentGateway()
        template = loader.get_template('fun/signup.html')
        welcome = 'Sign Up!'
        context = {'welcome': welcome}

        print('processing payment')
        print(request.session.items())
        for key, value in request.session.items():
            print('{} => {}'.format(key, value))

        if request.method == 'POST':
            # retrieve nonce
            nonce = request.POST.get('paymentMethodNonce', None)
=======

def process_payment(request):
    try:
        paymentGateway = PymentGateway()
        template = loader.get_template("fun/signup.html")
        welcome = "Sign Up!"
        context = {"welcome": welcome}

        print("processing payment")
        print(request.session.items())
        for key, value in request.session.items():
            print("{} => {}".format(key, value))

        if request.method == "POST":
            # retrieve nonce
            nonce = request.POST.get("paymentMethodNonce", None)
>>>>>>> a9be7de (commit and push everything)

        print("nonce:" + nonce)

        paymentGateway.chargePaymentMethod(nonce)

        print(context)
        return HttpResponse(template.render(context, request))

    except Exception as ex:
        print(ex.__str__())
        return signup(request)

<<<<<<< HEAD
def beautifuldata(request):
    try:
        template = loader.get_template('fun/beautifuldata.html')
        welcome = 'Data is Beautiful!'
=======

def beautifuldata(request):
    try:
        template = loader.get_template("fun/beautifuldata.html")
        welcome = "Data is Beautiful!"
>>>>>>> a9be7de (commit and push everything)

        helpView = HelpView()
        historicData = helpView.getHistoricCTARidershipData()
        predictiveData = helpView.getPredictiveCTARidershipData()
        dayOfWeekData = helpView.getDayOfWeekRidershipData()
        corrData = helpView.getCorrelationData()

<<<<<<< HEAD
        context = {'welcome': welcome, 'historic_dates': historicData['month'].tolist(),
                   'historic_rides': historicData['total_rides'].tolist(),
                   'predictive_dates': predictiveData['Month'].tolist(),
                   'predictive_rides': predictiveData['Ridership'].tolist(),
                   'days': dayOfWeekData['day'].tolist(),
                   'commutes_2022': dayOfWeekData['2022'].tolist(),
                   'commutes_2020': dayOfWeekData['2020'].tolist(),
                   'commutes_2019': dayOfWeekData['2019'].tolist(),
                   'commutes_2021': dayOfWeekData['2021'].tolist(),
                   'corr': corrData['Month'].tolist(),
                   'cta_rides': corrData['CTA Ridership'].tolist(),
                   'tnp_rides': corrData['TNP Trips'].tolist(),
                   'crashes': corrData['Crashes'].tolist()
                   }
=======
        context = {
            "welcome": welcome,
            "historic_dates": historicData["month"].tolist(),
            "historic_rides": historicData["total_rides"].tolist(),
            "predictive_dates": predictiveData["Month"].tolist(),
            "predictive_rides": predictiveData["Ridership"].tolist(),
            "days": dayOfWeekData["day"].tolist(),
            "commutes_2022": dayOfWeekData["2022"].tolist(),
            "commutes_2020": dayOfWeekData["2020"].tolist(),
            "commutes_2019": dayOfWeekData["2019"].tolist(),
            "commutes_2021": dayOfWeekData["2021"].tolist(),
            "corr": corrData["Month"].tolist(),
            "cta_rides": corrData["CTA Ridership"].tolist(),
            "tnp_rides": corrData["TNP Trips"].tolist(),
            "crashes": corrData["Crashes"].tolist(),
        }
>>>>>>> a9be7de (commit and push everything)

        # print(context)
        return HttpResponse(template.render(context, request))

    except Exception as ex:
        print(ex.__str__())
        return index(request)


def learn(request):
    try:
<<<<<<< HEAD
        template = loader.get_template('fun/learn.html')
        welcome = 'Let\'s Learn!'

        context = {'welcome': welcome}
=======
        template = loader.get_template("fun/learn.html")
        welcome = "Let's Learn!"

        context = {"welcome": welcome}
>>>>>>> a9be7de (commit and push everything)

        return HttpResponse(template.render(context, request))

    except Exception as ex:
        print(ex.__str__())
        return index(request)

<<<<<<< HEAD
def T4D7W(request):
    try:
        template = loader.get_template('fun/T4D7W.html')
        puzzle = 'T4D7W'

        context = {'puzzle': puzzle}
=======

def T4D7W(request):
    try:
        template = loader.get_template("fun/T4D7W.html")
        puzzle = "T4D7W"

        context = {"puzzle": puzzle}
>>>>>>> a9be7de (commit and push everything)

        return HttpResponse(template.render(context, request))

    except Exception as ex:
        print(ex.__str__())
        return index(request)


def lemonade(request):
    try:
<<<<<<< HEAD
        template = loader.get_template('fun/lemonade.html')
        welcome = 'Muy Bien Lemonade!'

        context = {'welcome': welcome}
=======
        template = loader.get_template("fun/lemonade.html")
        welcome = "Muy Bien Lemonade!"

        context = {"welcome": welcome}
>>>>>>> a9be7de (commit and push everything)

        return HttpResponse(template.render(context, request))

    except Exception as ex:
        print(ex.__str__())
        return index(request)

<<<<<<< HEAD
def hikethespike(request):
    try:
        template = loader.get_template('fun/hikethespike.html')
        welcome = 'Hike The Spike!'

        context = {'welcome': welcome}
=======

def hikethespike(request):
    try:
        template = loader.get_template("fun/hikethespike.html")
        welcome = "Hike The Spike!"

        context = {"welcome": welcome}
>>>>>>> a9be7de (commit and push everything)

        return HttpResponse(template.render(context, request))

    except Exception as ex:
        print(ex.__str__())
<<<<<<< HEAD
        return index(request)
=======
        return index(request)


def sns(request):
    try:
        template = loader.get_template("sns/adobe.html")
        welcome = "SNS!"

        context = {"welcome": welcome}

        return HttpResponse(template.render(context, request))

    except Exception as ex:
        print(ex.__str__())
        return index(request)
>>>>>>> a9be7de (commit and push everything)
