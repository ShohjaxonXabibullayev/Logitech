from django.shortcuts import render
from .models import Techs

def technos(request):
    techs = Techs.objects.all()
    return render(request, 'products.html', {'techs':techs})

