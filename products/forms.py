from django import forms
from .models import Techs

class TechsForm(forms.ModelForm):
    class Meta:
        model = Techs
        fields = ['user', 'category', 'title', 'camera', 'batareya', 'harakteri', 'deck',  'price', 'image']

