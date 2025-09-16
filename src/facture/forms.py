from django import forms
from .models import Client
class ClientRegisterForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom']
