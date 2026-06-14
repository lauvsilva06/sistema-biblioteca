from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from .models import Emprestimo
from acervo.models import Exemplar
from usuarios.models import PerfilUsuario


class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ['usuario', 'exemplar', 'data_prevista', 'observacoes']
        widgets = {
            'data_prevista': forms.DateInput(attrs={'type': 'date'}),
            'observacoes': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['usuario'].queryset = User.objects.filter(perfil__ativo=True, is_staff=False).order_by('first_name')
        self.fields['usuario'].label_from_instance = lambda u: f'{u.get_full_name()} (CPF: {u.perfil.cpf})'
        self.fields['exemplar'].queryset = Exemplar.objects.filter(disponivel=True).select_related('livro')
        self.fields['exemplar'].label_from_instance = lambda e: f'{e.livro.titulo} [{e.codigo}]'
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'usuario', 'exemplar',
            Row(Column('data_prevista', css_class='col-md-4')),
            'observacoes',
            Submit('submit', 'Registrar Empréstimo', css_class='btn btn-success mt-2')
        )

    def clean(self):
        cleaned_data = super().clean()
        usuario = cleaned_data.get('usuario')
        if usuario and hasattr(usuario, 'perfil') and usuario.perfil.tem_pendencias:
            raise forms.ValidationError(
                f'{usuario.get_full_name()} possui empréstimos em atraso. Regularize antes de novo empréstimo.'
            )
        return cleaned_data
