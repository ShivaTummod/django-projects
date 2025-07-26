from django import forms

FIELD_TYPES = [
    ('CharField', 'Text'),
    ('IntegerField', 'Number'),
    ('BooleanField', 'True/False'),
    ('DateField', 'Date'),
]

class UserFieldForm(forms.Form):
    field_name = forms.CharField(label="Field Name", max_length=100)
    field_type = forms.ChoiceField(label="Data Type", choices=FIELD_TYPES)
    field_value = forms.CharField(label="Value")

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(label="Upload CSV File")
