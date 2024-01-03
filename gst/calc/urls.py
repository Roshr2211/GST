# calc/urls.py

from django.urls import path
from . import views

app_name = 'calc'

urlpatterns = [
    path('', views.index, name='index'),
    # Add other URL patterns as needed
]


