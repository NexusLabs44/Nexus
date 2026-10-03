# ECONEXUS

Plataforma de calculo e acompanhamento de pegada de carbono.

## Estrutura

- `frontend/pages/`: paginas HTML da aplicacao.
- `frontend/assets/css/`: estilos.
- `frontend/assets/js/`: scripts do frontend.
- `frontend/assets/images/`: imagens e icones.
- `backend/`: projeto Django, modelos e configuracao do MySQL.
- `backend/accounts/`: usuario customizado e autenticacao.
- `backend/calculations/`: calculos e emissoes por categoria.

## Frontend

Abra `frontend/pages/index.html` para visualizar a interface estatica.

## Backend

Entre na pasta `backend`, configure o arquivo `.env` a partir de `.env.example`, instale as dependencias e execute as migrations conforme o [guia do backend](backend/README.md).

As credenciais do banco nao devem ser salvas neste repositorio.
