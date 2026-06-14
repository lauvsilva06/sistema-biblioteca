from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from datetime import timedelta


def prazo_padrao():
    dias = getattr(settings, 'PRAZO_EMPRESTIMO_DIAS', 14)
    return timezone.now().date() + timedelta(days=dias)


class Emprestimo(models.Model):
    exemplar = models.ForeignKey(
        'acervo.Exemplar', on_delete=models.PROTECT,
        related_name='emprestimos', verbose_name='Exemplar'
    )
    usuario = models.ForeignKey(
        User, on_delete=models.PROTECT,
        related_name='emprestimos', verbose_name='Usuário'
    )
    atendente = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='emprestimos_realizados', verbose_name='Atendente'
    )
    data_emprestimo = models.DateField('Data do Empréstimo', auto_now_add=True)
    data_prevista = models.DateField('Data Prevista de Devolução', default=prazo_padrao)
    data_devolucao = models.DateField('Data de Devolução', null=True, blank=True)
    observacoes = models.TextField('Observações', blank=True)

    class Meta:
        verbose_name = 'Empréstimo'
        verbose_name_plural = 'Empréstimos'
        ordering = ['-data_emprestimo']

    def __str__(self):
        return f'{self.usuario.get_full_name()} — {self.exemplar.livro.titulo}'

    @property
    def devolvido(self):
        return self.data_devolucao is not None

    @property
    def atrasado(self):
        if self.devolvido:
            return self.data_devolucao > self.data_prevista
        return timezone.now().date() > self.data_prevista

    @property
    def dias_atraso(self):
        if not self.atrasado:
            return 0
        referencia = self.data_devolucao if self.devolvido else timezone.now().date()
        return (referencia - self.data_prevista).days

    def registrar_devolucao(self):
        self.data_devolucao = timezone.now().date()
        self.exemplar.disponivel = True
        self.exemplar.save()
        self.save()
