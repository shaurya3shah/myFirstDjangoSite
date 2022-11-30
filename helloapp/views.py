from typing import Set

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

from helloapp.models import GuessedNumber


def index(request):
    template = loader.get_template('helloapp/index.html')
    guessed_number = GuessedNumber
    guessed_number.guessed_number = 10
    guessed_number.comparison = 'greater'

    context = {'gnumber': guessed_number}

    return HttpResponse(template.render(context, request))
