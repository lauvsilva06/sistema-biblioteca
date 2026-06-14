from django.db import models
from django.contrib.auth.models import User


class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    cpf = models.CharField('CPF', max_length=14, unique=True)
    telefone = models.CharField('Telefone', max_length=20, blank=True)
    endereco = models.TextField('Endereço', blank=True)
    data_nascimento = models.DateField('Data de Nascimento', null=True, blank=True)
    data_cadastro = models.DateField('Data de Cadastro', auto_now_add=True)
    ativo = models.BooleanField('Ativo', default=True)

    class Meta:
        verbose_name = 'Perfil de Usuário'
        verbose_name_plural = 'Perfis de Usuários'

    def __str__(self):
        return f'{self.user.get_full_name()} ({self.cpf})'

    @property
    def emprestimos_ativos(self):
        return self.user.emprestimos.filter(data_devolucao__isnull=True)

    @property
    def emprestimos_atrasados(self):
        from django.utils import timezone
        return self.user.emprestimos.filter(
            data_devolucao__isnull=True,
            data_prevista__lt=timezone.now().date()
        )

    @property
    def tem_pendencias(self):
        return self.emprestimos_atrasados.exists()
