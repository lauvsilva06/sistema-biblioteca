from django.contrib import admin
from .models import PerfilUsuario

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ['user', 'cpf', 'telefone', 'ativo', 'data_cadastro']
    list_filter = ['ativo']
    search_fields = ['user__first_name', 'user__last_name', 'cpf']
