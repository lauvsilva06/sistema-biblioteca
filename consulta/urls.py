from django.urls import path
from . import views

app_name = 'consulta'

urlpatterns = [
    path('', views.index, name='index'),
    path('buscar/', views.buscar, name='buscar'),
]
