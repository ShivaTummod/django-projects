from django.urls import path
from .views import dynamic_table_view, insert_into_table_view

urlpatterns = [
    path('create/', dynamic_table_view, name='create-table'),
    path('insert/', insert_into_table_view, name='insert-data'),
]
