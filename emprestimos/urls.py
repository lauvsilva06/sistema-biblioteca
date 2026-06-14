from django.urls import path
from . import views

app_name = 'emprestimos'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('emprestimos/', views.lista_emprestimos, name='lista_emprestimos'),
    path('emprestimos/novo/', views.novo_emprestimo, name='novo_emprestimo'),
    path('emprestimos/<int:pk>/devolver/', views.registrar_devolucao, name='registrar_devolucao'),
]
