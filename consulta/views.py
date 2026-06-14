from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from acervo.models import Livro, Assunto


def index(request):
    total_livros = Livro.objects.count()
    assuntos = Assunto.objects.all()[:12]
    destaques = Livro.objects.filter(exemplares__disponivel=True).distinct()[:6]
    return render(request, 'consulta/index.html', {
        'total_livros': total_livros,
        'assuntos': assuntos,
        'destaques': destaques,
    })


def buscar(request):
    q = request.GET.get('q', '').strip()
    assunto_id = request.GET.get('assunto', '')
    livros = Livro.objects.prefetch_related('exemplares', 'assuntos').all()

    if q:
        livros = livros.filter(
            Q(titulo__icontains=q) |
            Q(autor__icontains=q) |
            Q(assuntos__nome__icontains=q)
        ).distinct()

    if assunto_id:
        livros = livros.filter(assuntos__id=assunto_id)

    assuntos = Assunto.objects.all()
    paginator = Paginator(livros, 12)
    page = paginator.get_page(request.GET.get('page'))

    return render(request, 'consulta/buscar.html', {
        'page_obj': page,
        'q': q,
        'assunto_id': assunto_id,
        'assuntos': assuntos,
        'total': livros.count(),
    })
    
