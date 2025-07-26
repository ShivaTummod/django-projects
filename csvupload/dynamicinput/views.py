import csv
import io
from django.shortcuts import render, redirect
from .forms import UserFieldForm, CSVUploadForm
from .models import UserDatas

def user_input_view(request):
    manual_form = UserFieldForm()
    csv_form = CSVUploadForm()

    if request.method == 'POST':
        if 'submit_manual' in request.POST:
            manual_form = UserFieldForm(request.POST)
            if manual_form.is_valid():
                field_name = manual_form.cleaned_data['field_name']
                field_type = manual_form.cleaned_data['field_type']
                raw_value = manual_form.cleaned_data['field_value']

                try:
                    if field_type == 'IntegerField':
                        value = int(raw_value)
                    elif field_type == 'BooleanField':
                        value = str(raw_value).lower() in ['true', '1', 'yes']
                    else:
                        value = raw_value
                except Exception:
                    manual_form.add_error('field_value', f"Invalid value for type {field_type}")
                    return render(request, 'user_input.html', {
                        'manual_form': manual_form, 'csv_form': csv_form, 'data': UserDatas.objects.all()
                    })

                UserDatas.objects.create(
                    field_name=field_name,
                    field_type=field_type,
                    field_value=value
                )
                return redirect('user-form')

        elif 'submit_csv' in request.POST:
            csv_form = CSVUploadForm(request.POST, request.FILES)
            if csv_form.is_valid():
                try:
                    file = request.FILES['csv_file']
                    # Try UTF-8, fallback to Windows encoding
                    try:
                        content = file.read().decode('utf-8')
                    except UnicodeDecodeError:
                        file.seek(0)
                        content = file.read().decode('ISO-8859-1')

                    io_string = io.StringIO(content)
                    reader = csv.reader(io_string)
                    headers = next(reader, None)

                    if headers != ['field_name', 'field_type', 'field_value']:
                        csv_form.add_error('csv_file', 'CSV header must be: field_name,field_type,field_value')
                        return render(request, 'user_input.html', {
                            'manual_form': manual_form,
                            'csv_form': csv_form,
                            'data': UserDatas.objects.all()
                        })

                    rows_added = 0
                    for row in reader:
                        if len(row) != 3:
                            continue
                        field_name, field_type, field_value = row
                        UserDatas.objects.create(
                            field_name=field_name.strip(),
                            field_type=field_type.strip(),
                            field_value=field_value.strip()
                        )
                        rows_added += 1

                    if rows_added == 0:
                        csv_form.add_error('csv_file', 'No valid rows found in CSV.')
                    return redirect('user-form')

                except Exception as e:
                    csv_form.add_error('csv_file', f"Error processing CSV: {e}")

    return render(request, 'user_input.html', {
        'manual_form': manual_form,
        'csv_form': csv_form,
        'data': UserDatas.objects.all()
    })
