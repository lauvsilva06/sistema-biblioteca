from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Field
from .models import Livro, Exemplar


class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'isbn', 'editora', 'ano_publicacao',
                  'assuntos', 'sinopse', 'capa', 'eh_doacao', 'doador']
        widgets = {
            'sinopse': forms.Textarea(attrs={'rows': 3}),
            'assuntos': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(Column('titulo', css_class='col-md-8'), Column('autor', css_class='col-md-4')),
            Row(Column('isbn', css_class='col-md-4'), Column('editora', css_class='col-md-5'), Column('ano_publicacao', css_class='col-md-3')),
            'assuntos', 'sinopse', 'capa',
            Row(Column('eh_doacao', css_class='col-md-3'), Column('doador', css_class='col-md-9')),
            Submit('submit', 'Salvar Livro', css_class='btn btn-success mt-2')
        )


class ExemplarForm(forms.ModelForm):
    class Meta:
        model = Exemplar
        fields = ['codigo', 'condicao']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(Column('codigo', css_class='col-md-6'), Column('condicao', css_class='col-md-6')),
            Submit('submit', 'Adicionar Exemplar', css_class='btn btn-success mt-2')
        )
