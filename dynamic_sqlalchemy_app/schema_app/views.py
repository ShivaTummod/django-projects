from django.shortcuts import render
from .forms import FieldForm, InsertForm
from .utils import create_dynamic_table, insert_record
from sqlalchemy_config import get_sqlalchemy_engine  # ✅ REQUIRED import

def dynamic_table_view(request):
    message = ''
    if request.method == 'POST':
        form = FieldForm(request.POST)
        if form.is_valid():
            table_name = form.cleaned_data['table_name']
            fields = []
            f1 = form.cleaned_data['field1_name']
            t1 = form.cleaned_data['field1_type']
            fields.append({'name': f1, 'type': t1})
            f2 = form.cleaned_data.get('field2_name')
            t2 = form.cleaned_data.get('field2_type')
            if f2 and t2:
                fields.append({'name': f2, 'type': t2})

            create_dynamic_table(table_name, fields)
            message = f"✅ Table '{table_name}' created with fields!"
    else:
        form = FieldForm()
    return render(request, 'create_table.html', {'form': form, 'msg': message})

def insert_into_table_view(request):
    message = ''
    if request.method == 'POST':
        form = InsertForm(request.POST)
        if form.is_valid():
            table_name = form.cleaned_data['table_name']
            key = form.cleaned_data['key']
            value = form.cleaned_data['value']

            from sqlalchemy import MetaData, Table
            engine = get_sqlalchemy_engine()  # ✅ Now this works
            metadata = MetaData()
            table = Table(table_name, metadata, autoload_with=engine)

            insert_record(table, {key: value})
            message = f"✅ Inserted into '{table_name}': {key} = {value}"
    else:
        form = InsertForm()
    return render(request, 'insert_data.html', {'form': form, 'msg': message})
