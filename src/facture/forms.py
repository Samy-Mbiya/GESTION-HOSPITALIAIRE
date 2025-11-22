from django import forms
from .models import Client, Description,Facture, Nh


#===========CLIENT============
class ClientRegisterForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom']

#===========FACTURE============

#Enregistrement
class FactureForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = []
# Modification
class FacUpdateForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = ['acompte', 'remise']

#===========NOTE D'HONORAIRE============
#Enregistrement
class NhForm(forms.ModelForm):
    class Meta:
        model = Nh
        fields = []

# Modification
class NhUpdateForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = ['acompte', 'remise']

#===========DESCRIPTION============
#Enregistrement
class DescriptionForm(forms.ModelForm):
    class Meta:
        model = Description
        fields = ['detail', 'qt', 'prix']
        widgets = {
            'detail': forms.TextInput(attrs={'class': 'form-control'}),
            'qt': forms.NumberInput(attrs={'class': 'form-control'}),
            'prix': forms.NumberInput(attrs={'class': 'form-control'}),
        }

#Modification
class DescriptionUpdatForm(forms.ModelForm):
    class Meta:
        model = Description
        fields = ['detail', 'qt', 'prix']
        widgets = {
            'detail': forms.TextInput(attrs={'class': 'form-control'}),
            'qt': forms.NumberInput(attrs={'class': 'form-control'}),
            'prix': forms.NumberInput(attrs={'class': 'form-control'}),
        }
