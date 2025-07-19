from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('Aloqa/', contact, name='contact'),
    path('Biz haqimizda/', about, name='about')
]

