from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Livro, Exemplar, Assunto
from .forms import LivroForm, ExemplarForm


def is_staff(user):
    return user.is_staff


@login_required
@user_passes_test(is_staff)
def lista_livros(request):
    livros = Livro.objects.prefetch_related('exemplares', 'assuntos').all()
    q = request.GET.get('q', '')
    if q:
        livros = livros.filter(titulo__icontains=q) | livros.filter(autor__icontains=q)
    paginator = Paginator(livros, 20)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'acervo/lista_livros.html', {'page_obj': page, 'q': q})


@login_required
@user_passes_test(is_staff)
def cadastrar_livro(request):
    form = LivroForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        livro = form.save()
        messages.success(request, f'Livro "{livro.titulo}" cadastrado com sucesso!')
        return redirect('acervo:lista_livros')
    return render(request, 'acervo/form_livro.html', {'form': form, 'titulo': 'Cadastrar Livro'})


@login_required
@user_passes_test(is_staff)
def editar_livro(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    form = LivroForm(request.POST or None, request.FILES or None, instance=livro)
    if form.is_valid():
        form.save()
        messages.success(request, 'Livro atualizado com sucesso!')
        return redirect('acervo:lista_livros')
    return render(request, 'acervo/form_livro.html', {'form': form, 'titulo': 'Editar Livro', 'livro': livro})


@login_required
@user_passes_test(is_staff)
def detalhe_livro(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    exemplares = livro.exemplares.all()
    return render(request, 'acervo/detalhe_livro.html', {'livro': livro, 'exemplares': exemplares})


@login_required
@user_passes_test(is_staff)
def adicionar_exemplar(request, livro_pk):
    livro = get_object_or_404(Livro, pk=livro_pk)
    form = ExemplarForm(request.POST or None)
    if form.is_valid():
        exemplar = form.save(commit=False)
        exemplar.livro = livro
        exemplar.save()
        messages.success(request, 'Exemplar adicionado com sucesso!')
        return redirect('acervo:detalhe_livro', pk=livro.pk)
    return render(request, 'acervo/form_exemplar.html', {'form': form, 'livro': livro})
