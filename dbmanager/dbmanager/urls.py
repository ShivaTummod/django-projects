"""
URL configuration for dbmanager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from database import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create-table/', views.create_table, name='create_table'),
    path('add-column/<str:table_name>/', views.add_column, name='add_column'),
    path('insert-data/<str:table_name>/', views.insert_data, name='insert_data'),
    path('upload-csv/<str:table_name>/', views.upload_csv, name='upload_csv'),
    path('audit-log/', views.audit_log_view, name='audit_log'),
]
