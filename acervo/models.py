from django.db import models


class Assunto(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Assunto'
        verbose_name_plural = 'Assuntos'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Livro(models.Model):
    titulo = models.CharField('Título', max_length=300)
    autor = models.CharField('Autor', max_length=200)
    isbn = models.CharField('ISBN', max_length=13, unique=True, blank=True, null=True)
    editora = models.CharField('Editora', max_length=200, blank=True)
    ano_publicacao = models.PositiveIntegerField('Ano de Publicação', null=True, blank=True)
    assuntos = models.ManyToManyField(Assunto, blank=True, verbose_name='Assuntos')
    sinopse = models.TextField('Sinopse', blank=True)
    capa = models.ImageField('Capa', upload_to='capas/', null=True, blank=True)
    eh_doacao = models.BooleanField('É doação?', default=False)
    doador = models.CharField('Nome do Doador', max_length=200, blank=True)
    data_cadastro = models.DateField('Data de Cadastro', auto_now_add=True)

    class Meta:
        verbose_name = 'Livro'
        verbose_name_plural = 'Livros'
        ordering = ['titulo']

    def __str__(self):
        return f'{self.titulo} — {self.autor}'

    @property
    def total_exemplares(self):
        return self.exemplares.count()

    @property
    def exemplares_disponiveis(self):
        return self.exemplares.filter(disponivel=True).count()


class Exemplar(models.Model):
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, related_name='exemplares')
    codigo = models.CharField('Código do Exemplar', max_length=50, unique=True)
    disponivel = models.BooleanField('Disponível', default=True)
    condicao = models.CharField('Condição', max_length=50, choices=[
        ('otimo', 'Ótimo'),
        ('bom', 'Bom'),
        ('regular', 'Regular'),
        ('ruim', 'Ruim'),
    ], default='bom')
    data_aquisicao = models.DateField('Data de Aquisição', auto_now_add=True)

    class Meta:
        verbose_name = 'Exemplar'
        verbose_name_plural = 'Exemplares'

    def __str__(self):
        return f'{self.codigo} — {self.livro.titulo}'
