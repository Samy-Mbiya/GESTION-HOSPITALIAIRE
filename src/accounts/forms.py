from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Utilisateur


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class RoleUpdateForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['role']