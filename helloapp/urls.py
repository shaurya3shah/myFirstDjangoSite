from django.urls import path

from . import views

app_name = 'helloapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('check_guess', views.check_guess, name='check_guess')
]