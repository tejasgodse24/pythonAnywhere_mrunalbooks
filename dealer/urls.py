from django.contrib import admin
from django.urls import path, include
from dealer.views import *


urlpatterns = [
    path('register/' ,  dealer_register, name='dealer_register'),
    path('login/' ,  dealer_login, name='dealer_login'),
    path('get-names/',  get_dealer_names_ajax, name='get_dealer_names_ajax'),
] 
