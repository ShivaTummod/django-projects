from django import forms

class AddColumnForm(forms.Form):
    column_name = forms.CharField(max_length=100)
    data_type = forms.ChoiceField(choices=[
        ('String', 'String'),
        ('Integer', 'Integer'),
        ('Float', 'Float'),
        ('Boolean', 'Boolean'),
        ('Date', 'Date'),
    ])