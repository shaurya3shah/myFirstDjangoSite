import random
from typing import Set

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

from helloapp.models import GuessedNumber

secret_number: int = 0
check_count: int = 0


def index(request):
    template = loader.get_template('helloapp/index.html')
    global secret_number
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
