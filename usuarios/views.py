from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from .models import PerfilUsuario
from .forms import LoginForm, CadastroUsuarioForm


def is_staff(user):
    return user.is_staff


def login_view(request):
    if request.user.is_authenticated:
        return redirect('emprestimos:dashboard')
    form = LoginForm(request.POST or None)
    if form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        if user and user.is_staff:
            login(request, user)
            return redirect(request.GET.get('next', 'emprestimos:dashboard'))
        messages.error(request, 'Credenciais inválidas ou sem permissão de acesso.')
    return render(request, 'usuarios/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('consulta:index')


@login_required
@user_passes_test(is_staff)
def lista_usuarios(request):
    usuarios = PerfilUsuario.objects.select_related('user').all()
    q = request.GET.get('q', '')
    if q:
        usuarios = usuarios.filter(user__first_name__icontains=q) | \
                   usuarios.filter(user__last_name__icontains=q) | \
                   usuarios.filter(cpf__icontains=q)
    paginator = Paginator(usuarios, 20)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'usuarios/lista_usuarios.html', {'page_obj': page, 'q': q})


@login_required
@user_passes_test(is_staff)
def cadastrar_usuario(request):
    form = CadastroUsuarioForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        messages.success(request, f'Usuário {user.get_full_name()} cadastrado com sucesso!')
        return redirect('usuarios:lista_usuarios')
    return render(request, 'usuarios/form_usuario.html', {'form': form, 'titulo': 'Cadastrar Usuário'})


@login_required
@user_passes_test(is_staff)
def perfil_usuario(request, pk):
    perfil = get_object_or_404(PerfilUsuario, pk=pk)
    emprestimos_ativos = perfil.emprestimos_ativos
    historico = perfil.user.emprestimos.filter(data_devolucao__isnull=False).order_by('-data_devolucao')[:10]
    return render(request, 'usuarios/perfil_usuario.html', {
        'perfil': perfil,
        'emprestimos_ativos': emprestimos_ativos,
        'historico': historico,
    })
