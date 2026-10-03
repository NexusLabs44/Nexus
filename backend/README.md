# Backend Django da ECONEXUS

## Estrutura

- `config/`: configuracoes do projeto Django.
- `accounts/`: usuario customizado com login por e-mail.
- `calculations/`: calculos, detalhes de pessoa fisica/juridica e emissoes.
- `.env.example`: variaveis necessarias para conectar ao MySQL do Railway.

## Configuracao local

1. Instale o Python 3.12 ou superior.
2. Crie um ambiente virtual dentro de `backend`.
3. Instale as dependencias com `pip install -r requirements.txt`.
4. Copie `.env.example` para `.env`.
5. Preencha o `.env` com as credenciais atuais do Railway, usando uma senha rotacionada.
6. Gere as migrations com `python manage.py makemigrations`.
7. Aplique-as com `python manage.py migrate`.
8. Crie o administrador com `python manage.py createsuperuser`.
9. Inicie com `python manage.py runserver`.

As credenciais reais nao devem ser commitadas. O arquivo `.env` ja esta ignorado pelo Git.