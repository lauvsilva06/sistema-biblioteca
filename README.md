# Biblioteca Pública Municipal de Gravatá — Sistema Web

Projeto extensionista desenvolvido para a Biblioteca Pública Municipal de Gravatá/PE.

## Funcionalidades

- **Consulta pública**: busca de livros por título, autor e assunto
- **Gerenciamento de acervo**: cadastro de livros, doações e exemplares
- **Controle de empréstimos**: registro, prazos e devoluções
- **Detecção de atrasos**: identificação automática de empréstimos vencidos
- **Perfil de usuário**: histórico completo por leitor

## Tecnologias

- Python 3.11 + Django 4.2
- PostgreSQL (produção) / SQLite (desenvolvimento)
- Bootstrap 5 + Bootstrap Icons

## Instalação Local

```bash
git clone <seu-repositório>
cd biblioteca_gravata
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
cp .env.example .env      # configure as variáveis
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Deploy no Railway

1. Crie uma conta em railway.app
2. Novo projeto → Deploy from GitHub
3. Adicione um serviço PostgreSQL
4. Configure as variáveis de ambiente (`.env.example`)
5. Deploy automático a cada push

## Estrutura

```
acervo/       → Livros, exemplares, assuntos
usuarios/     → Perfis e autenticação
emprestimos/  → Controle de empréstimos
consulta/     → Interface pública
```
