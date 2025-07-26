import os
from django.shortcuts import render
from .forms import FieldInputForm

def create_model_view(request):
    msg = ''
    if request.method == 'POST':
        form = FieldInputForm(request.POST)
        if form.is_valid():
            model_name = form.cleaned_data['model_name']
            field_name = form.cleaned_data['field_name']
            field_type = form.cleaned_data['field_type']

            # Handle defaults
            default_value = {
                "CharField": "''",
                "IntegerField": "0",
                "TextField": "''",
                "BooleanField": "False",
                "DateField": "'2000-01-01'",
            }[field_type]

            # Create the field string
            if field_type == "CharField":
                field_definition = f"{field_name} = models.{field_type}(max_length=255, default={default_value})"
            else:
                field_definition = f"{field_name} = models.{field_type}(default={default_value})"

            # Build full model code
            model_str = f"""from django.db import models

class {model_name}(models.Model):
    {field_definition}
"""

            # Write to models_generated.py
            with open("dynamicmodel/models_generated.py", "w") as f:
                f.write(model_str)

            # Append to models.py (if not already present)
            with open("dynamicmodel/models.py", "r") as f:
                models_py_content = f.read()

            import_line = f"from .models_generated import {model_name}"
            if import_line not in models_py_content:
                with open("dynamicmodel/models.py", "a") as f:
                    f.write(f"\n{import_line}")

            # Run migrations
            os.system("python manage.py makemigrations dynamicmodel")
            os.system("python manage.py migrate dynamicmodel")

            msg = f"✅ Model `{model_name}` with field `{field_name}` ({field_type}) created successfully with default value!"
    else:
        form = FieldInputForm()

    return render(request, "create_model.html", {"form": form, "msg": msg})
