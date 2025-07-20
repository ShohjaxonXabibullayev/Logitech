from django import forms
from .models import Techs
from .models import Comment
from django.contrib.auth.models import User

class TechsForm(forms.ModelForm):
    class Meta:
        model = Techs
        fields = ['user', 'category', 'title', 'camera', 'batareya', 'harakteri', 'deck',  'price', 'image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Ismingiz'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Familiyangiz'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email manzilingiz'}),
        }


