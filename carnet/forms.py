from django import forms
from .models import *


class CompteForm(forms.ModelForm):

    numero = forms.CharField(widget=forms.TextInput(attrs={
                'class':'form-control',
                'type':'text',
                'id':'input_numero',
                'placeholder':'Entree numero',
                'onkeypress':'return myFunction2()',
                'required':''
    }))

    numOrganisation = forms.CharField(required=False,widget=forms.TextInput(attrs={
                'class': 'form-control',
                'type':'text',
                'id': 'myInput',
                'placeholder': 'Entree numero dorganisation',
                'onkeypress':'return myFunction()',
    }))

    libelle = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'placeholder': 'Entree labelle',
        'class': 'form-control',
        'required': ''
    }))
    class Meta:
        model = Compte
        fields = '__all__'


# class CarnetForm(forms.ModelForm):
#     compte = forms.Select(widget=forms.TextInput(attrs={}))

    # class Meta:
    #     model = CarnetCheque
    #     fields = '__all__'