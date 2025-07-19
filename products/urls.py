from django.urls import path
from .views import *

urlpatterns = [
    path('', technos, name='products-list')
]