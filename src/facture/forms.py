from django import forms
from .models import Client, Description,Facture, Nh


#CLIENT
#-------
class ClientRegisterForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom']

#FACTURE
#-------
# Creation
class FactureForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = []

# Modification
class FacUpdateForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = ['acompte', 'remise']

class NhForm(forms.ModelForm):
    class Meta:
        model = Nh
        fields = ['client', 'acompte', 'remise']
        widgets = {
            'client': forms.TextInput(attrs={'class': 'form-control'}),
            'acompte': forms.NumberInput(attrs={'class': 'form-control'}),
            'remise': forms.NumberInput(attrs={'class': 'form-control'}),
        }

#Description Enregistre
class DescriptionForm(forms.ModelForm):
    class Meta:
        model = Description
        fields = ['detail', 'qt', 'prix']
        widgets = {
            'detail': forms.TextInput(attrs={'class': 'form-control'}),
            'qt': forms.NumberInput(attrs={'class': 'form-control'}),
            'prix': forms.NumberInput(attrs={'class': 'form-control'}),
        }

#Description Update
class DescriptionUpdatForm(forms.ModelForm):
    class Meta:
        model = Description
        fields = ['detail', 'qt', 'prix']
        widgets = {
            'detail': forms.TextInput(attrs={'class': 'form-control'}),
            'qt': forms.NumberInput(attrs={'class': 'form-control'}),
            'prix': forms.NumberInput(attrs={'class': 'form-control'}),
        }
