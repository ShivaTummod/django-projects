from django import forms

FIELD_TYPES = [
    ('CharField', 'CharField'),
    ('IntegerField', 'IntegerField'),
    ('TextField', 'TextField'),
    ('BooleanField', 'BooleanField'),
    ('DateField', 'DateField'),
]

class FieldInputForm(forms.Form):
    model_name = forms.CharField(label='Model Name', max_length=50)
    field_name = forms.CharField(label='Field Name', max_length=50)
    field_type = forms.ChoiceField(label='Field Type', choices=FIELD_TYPES)
