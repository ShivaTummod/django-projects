from django.shortcuts import render, redirect
from .sqlalchemy_helper import *
from .forms import AddColumnForm
from .models import AuditLog
import pandas as pd
from sqlalchemy import Table
from sqlalchemy.sql.sqltypes import Integer, Float, Boolean, Date
from datetime import datetime


def dashboard(request):
    tables = list_tables()
    return render(request, 'database/dashboard.html', {'tables': tables})

def create_table(request):
    if request.method == 'POST':
        name = request.POST['table_name']
        create_custom_table(name)
        AuditLog.objects.create(table_name=name, action='CREATE TABLE')
        return redirect('dashboard')
    return render(request, 'database/create_table.html')

def add_column(request, table_name):
    form = AddColumnForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        add_column(
            table_name,
            form.cleaned_data['column_name'],
            form.cleaned_data['data_type'],
        )
        AuditLog.objects.create(table_name=table_name, action='ADD COLUMN', description=form.cleaned_data['column_name'])
        return redirect('dashboard')
    return render(request, 'database/add_column.html', {'form': form, 'table': table_name})

def insert_data(request, table_name):
    table = Table(table_name, metadata, autoload_with=engine)
    column_types = {col.name: col.type for col in table.columns if col.name != 'id'}
    if request.method == 'POST':
        data = {}
        for col in column_types:
            val = request.POST.get(col)
            if isinstance(column_types[col], Integer):
                data[col] = int(val) if val else None
            elif isinstance(column_types[col], Float):
                data[col] = float(val) if val else None
            elif isinstance(column_types[col], Boolean):
                data[col] = val.lower() in ['true', '1', 'yes', 'on']
            elif isinstance(column_types[col], Date):
                data[col] = datetime.strptime(val, "%Y-%m-%d").date() if val else None
            else:
                data[col] = val
        insert_row(table_name, data)
        AuditLog.objects.create(table_name=table_name, action='INSERT ROW')
        return redirect('dashboard')
    return render(request, 'database/insert_data.html', {'columns': column_types.keys(), 'table': table_name})

def upload_csv(request, table_name):
    if request.method == 'POST':
        df = pd.read_csv(request.FILES['csv_file'])
        if 'confirm' in request.POST:
            insert_csv_data(table_name, df)
            AuditLog.objects.create(table_name=table_name, action='CSV UPLOAD')
            return redirect('dashboard')
        preview = df.head(5).to_dict(orient='records')
        return render(request, 'database/upload_csv.html', {'preview': preview, 'table': table_name})
    return render(request, 'database/upload_csv.html', {'table': table_name})

def audit_log_view(request):
    logs = AuditLog.objects.all().order_by('-timestamp')
    return render(request, 'database/audit_log.html', {'logs': logs})