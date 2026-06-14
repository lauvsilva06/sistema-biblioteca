from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Emprestimo
from .forms import EmprestimoForm
from acervo.models import Exemplar


def is_staff(user):
    return user.is_staff


@login_required
@user_passes_test(is_staff)
def dashboard(request):
    hoje = timezone.now().date()
    total_emprestimos = Emprestimo.objects.filter(data_devolucao__isnull=True).count()
    atrasados = Emprestimo.objects.filter(data_devolucao__isnull=True, data_prevista__lt=hoje)
    vencendo_hoje = Emprestimo.objects.filter(data_devolucao__isnull=True, data_prevista=hoje)
    recentes = Emprestimo.objects.select_related('usuario', 'exemplar__livro').order_by('-data_emprestimo')[:8]
    return render(request, 'emprestimos/dashboard.html', {
        'total_emprestimos': total_emprestimos,
        'total_atrasados': atrasados.count(),
        'vencendo_hoje': vencendo_hoje.count(),
        'atrasados': atrasados.select_related('usuario', 'exemplar__livro')[:5],
        'recentes': recentes,
        'hoje': hoje,
    })


@login_required
@user_passes_test(is_staff)
def lista_emprestimos(request):
    emprestimos = Emprestimo.objects.select_related('usuario', 'exemplar__livro').all()
    status = request.GET.get('status', '')
    q = request.GET.get('q', '')
    hoje = timezone.now().date()

    if status == 'ativos':
        emprestimos = emprestimos.filter(data_devolucao__isnull=True)
    elif status == 'atrasados':
        emprestimos = emprestimos.filter(data_devolucao__isnull=True, data_prevista__lt=hoje)
    elif status == 'devolvidos':
        emprestimos = emprestimos.filter(data_devolucao__isnull=False)

    if q:
        emprestimos = emprestimos.filter(
            Q(usuario__first_name__icontains=q) |
            Q(usuario__last_name__icontains=q) |
            Q(exemplar__livro__titulo__icontains=q)
        )

    paginator = Paginator(emprestimos, 20)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'emprestimos/lista_emprestimos.html', {
        'page_obj': page, 'status': status, 'q': q, 'hoje': hoje
    })


@login_required
@user_passes_test(is_staff)
def novo_emprestimo(request):
    form = EmprestimoForm(request.POST or None)
    if form.is_valid():
        emprestimo = form.save(commit=False)
        emprestimo.atendente = request.user
        emprestimo.exemplar.disponivel = False
        emprestimo.exemplar.save()
        emprestimo.save()
        messages.success(request, f'Empréstimo registrado para {emprestimo.usuario.get_full_name()}!')
        return redirect('emprestimos:lista_emprestimos')
    return render(request, 'emprestimos/form_emprestimo.html', {'form': form})


@login_required
@user_passes_test(is_staff)
def registrar_devolucao(request, pk):
    emprestimo = get_object_or_404(Emprestimo, pk=pk)
    if emprestimo.devolvido:
        messages.warning(request, 'Este empréstimo já foi devolvido.')
        return redirect('emprestimos:lista_emprestimos')
    if request.method == 'POST':
        emprestimo.registrar_devolucao()
        if emprestimo.atrasado:
            messages.warning(request, f'Devolução registrada com {emprestimo.dias_atraso} dia(s) de atraso.')
        else:
            messages.success(request, 'Devolução registrada com sucesso!')
        return redirect('emprestimos:lista_emprestimos')
    return render(request, 'emprestimos/confirmar_devolucao.html', {'emprestimo': emprestimo})
