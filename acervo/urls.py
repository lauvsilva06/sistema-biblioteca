from django.urls import path
from . import views

app_name = 'acervo'

urlpatterns = [
    path('', views.lista_livros, name='lista_livros'),
    path('cadastrar/', views.cadastrar_livro, name='cadastrar_livro'),
    path('<int:pk>/', views.detalhe_livro, name='detalhe_livro'),
    path('<int:pk>/editar/', views.editar_livro, name='editar_livro'),
    path('<int:livro_pk>/exemplar/adicionar/', views.adicionar_exemplar, name='adicionar_exemplar'),
]
