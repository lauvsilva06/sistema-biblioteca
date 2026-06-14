from django.contrib import admin
from .models import Assunto, Livro, Exemplar

@admin.register(Assunto)
class AssuntoAdmin(admin.ModelAdmin):
    list_display = ['nome']
    search_fields = ['nome']

class ExemplarInline(admin.TabularInline):
    model = Exemplar
    extra = 1

@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'isbn', 'eh_doacao', 'data_cadastro']
    list_filter = ['eh_doacao', 'assuntos']
    search_fields = ['titulo', 'autor', 'isbn']
    inlines = [ExemplarInline]

@admin.register(Exemplar)
class ExemplarAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'livro', 'disponivel', 'condicao']
    list_filter = ['disponivel', 'condicao']
