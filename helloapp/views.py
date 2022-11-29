from typing import Set

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader


def index(request):
    template = loader.get_template('helloapp/index.html')
    return HttpResponse(template.render())