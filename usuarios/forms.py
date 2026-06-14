from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from .models import PerfilUsuario


class LoginForm(forms.Form):
    username = forms.CharField(label='Usuário')
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout('username', 'password', Submit('submit', 'Entrar', css_class='btn btn-primary w-100 mt-2'))


class CadastroUsuarioForm(forms.Form):
    first_name = forms.CharField(label='Nome')
    last_name = forms.CharField(label='Sobrenome')
    username = forms.CharField(label='Login')
    email = forms.EmailField(label='E-mail', required=False)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)
    cpf = forms.CharField(label='CPF', max_length=14)
    telefone = forms.CharField(label='Telefone', required=False)
    endereco = forms.CharField(label='Endereço', widget=forms.Textarea(attrs={'rows': 2}), required=False)
    data_nascimento = forms.DateField(label='Data de Nascimento', required=False,
                                      widget=forms.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(Column('first_name', css_class='col-md-6'), Column('last_name', css_class='col-md-6')),
            Row(Column('username', css_class='col-md-5'), Column('email', css_class='col-md-7')),
            Row(Column('password', css_class='col-md-6'), Column('cpf', css_class='col-md-6')),
            Row(Column('telefone', css_class='col-md-6'), Column('data_nascimento', css_class='col-md-6')),
            'endereco',
            Submit('submit', 'Cadastrar Usuário', css_class='btn btn-success mt-2')
        )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Este nome de usuário já está em uso.')
        return username

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        if PerfilUsuario.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError('Este CPF já está cadastrado.')
        return cpf

    def save(self):
        data = self.cleaned_data
        user = User.objects.create_user(
            username=data['username'], email=data.get('email', ''),
            password=data['password'], first_name=data['first_name'], last_name=data['last_name']
        )
        PerfilUsuario.objects.create(
            user=user, cpf=data['cpf'], telefone=data.get('telefone', ''),
            endereco=data.get('endereco', ''), data_nascimento=data.get('data_nascimento')
        )
        return user
