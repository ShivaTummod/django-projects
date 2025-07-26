from django import forms

class FieldForm(forms.Form):
    table_name = forms.CharField()
    field1_name = forms.CharField()
    field1_type = forms.ChoiceField(choices=[('string', 'String'), ('int', 'Integer'), ('float', 'Float'), ('date', 'Date')])
    field2_name = forms.CharField(required=False)
    field2_type = forms.ChoiceField(choices=[('string', 'String'), ('int', 'Integer'), ('float', 'Float'), ('date', 'Date')], required=False)

class InsertForm(forms.Form):
    table_name = forms.CharField()
    key = forms.CharField()
    value = forms.CharField()
