from django.urls import path
from . import views  # assuming your views module is named 'views'

app_name = 'calc'

urlpatterns = [
    path('', views.index, name='index'),
    path('', views.select_column, name='select_column'),
    # Add other URL patterns as needed
]



