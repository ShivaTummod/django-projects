from django import forms
from .models import InputTable

class InputForm(forms.ModelForm):
    class Meta:
        model = InputTable
        fields = ['name', 'email', 'contact', 'flat_price', 'square_feet']