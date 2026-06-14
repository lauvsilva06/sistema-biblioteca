from django.contrib import admin
from .models import Emprestimo

@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'exemplar', 'data_emprestimo', 'data_prevista', 'data_devolucao']
    list_filter = ['data_emprestimo', 'data_devolucao']
    search_fields = ['usuario__first_name', 'exemplar__livro__titulo']
