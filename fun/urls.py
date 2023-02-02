from django.urls import path

from . import views

app_name = 'fun'
urlpatterns = [
    path('', views.index, name='index'),
    path('guess_number', views.guess_number, name='guess_number'),
    path('check_guess', views.check_guess, name='check_guess'),
    path('crazy_libs', views.crazy_libs, name='crazy_libs'),
    path('generate_crazy_libs', views.generate_crazy_libs, name='generate_crazy_libs'),
    path('numberdle', views.numberdle, name='numberdle'),
    path('check_numberdle', views.check_numberdle, name='check_numberdle'),
    path('countries_connection', views.countries_connection, name='countries_connection'),
    path('connect_country', views.connect_country, name='connect_country'),
    path('spelling_bee', views.spelling_bee, name='spelling_bee'),
    path('spell_check', views.spell_check, name='spell_check'),
    path('spell_new', views.spell_new, name='spell_new'),
    path('feedback', views.feedback, name='feedback'),
    path('stocks', views.stocks, name='stocks'),
    path('sorting_hat', views.sorting_hat, name='sorting_hat'),
    path('sorting_hat_admin', views.sorting_hat_admin, name='sorting_hat_admin')
]