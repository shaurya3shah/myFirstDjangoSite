from django.urls import path

from . import views

app_name = 'helloapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('check_guess', views.check_guess, name='check_guess'),
    path('crazy_libs', views.crazy_libs, name='crazy_libs'),
    path('generate_crazy_libs', views.generate_crazy_libs, name='generate_crazy_libs')
]