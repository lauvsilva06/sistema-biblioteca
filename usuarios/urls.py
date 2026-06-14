from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.lista_usuarios, name='lista_usuarios'),
    path('cadastrar/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('<int:pk>/', views.perfil_usuario, name='perfil_usuario'),
]
