# Catalog API

API REST simples, construída com **FastAPI** e **SQLModel**, para consulta e gerenciamento de itens de um catálogo (produtos, peças, materiais etc). Projeto feito para portfólio, com estrutura organizada e documentação automática via Swagger.

Itens criados sem `image_url` recebem automaticamente uma imagem genérica (gerada de forma determinística a partir do nome do item), só para deixar a listagem mais visual sem depender de upload de arquivos.

## Funcionalidades

- Interface web simples (HTML/CSS/JS puro) para visualizar e gerenciar o catálogo visualmente
- Listagem de itens com filtro por categoria e paginação
- Busca de item por id
- Criação, atualização parcial e remoção de itens
- Banco de dados SQLite criado automaticamente, com alguns itens de exemplo (seed) na primeira execução
- Documentação interativa automática (Swagger UI e ReDoc)

## Tecnologias

- Python 3.10+
- FastAPI
- SQLModel (Pydantic + SQLAlchemy)
- SQLite
- Uvicorn

## Estrutura do projeto

```
catalog-api/
├── app/
│   ├── main.py          # instância da aplicação, seed de dados e rota de health-check
│   ├── database.py      # configuração da engine e da sessão do banco
│   ├── models.py        # modelo de tabela (SQLModel)
│   ├── schemas.py       # schemas de entrada/saída (Pydantic)
│   ├── crud.py          # funções de acesso a dados
│   ├── utils.py         # geração de imagens genéricas
│   ├── static/          # interface web (HTML/CSS/JS) servida na raiz "/"
│   └── routers/
│       └── items.py     # rotas de /items
├── requirements.txt
└── README.md
```

## Como rodar
n
```bash
# clonar o repositório
git clone https://github.com/jadineigxavier/API-REST-de-Cat-logo-de-Produtos
cd catalog-api

# criar e ativar um ambiente virtual
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# instalar dependências
pip install -r requirements.txt

# subir o servidor
uvicorn app.main:app --reload
```

A API sobe em `http://127.0.0.1:8000`:

- **Interface web (catálogo visual):** `http://127.0.0.1:8000/`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Endpoints

| Método | Rota            | Descrição                                          |
|--------|-----------------|------------------------------------------------------|
| GET    | `/`             | Interface web do catálogo                            |
| GET    | `/items`        | Lista itens (filtros: `category`, `skip`, `limit`)   |
| GET    | `/items/{id}`   | Retorna um item pelo id                              |
| POST   | `/items`        | Cria um novo item                                    |
| PUT    | `/items/{id}`   | Atualiza um item existente (parcial)                 |
| DELETE | `/items/{id}`   | Remove um item                                       |
| GET    | `/api/health`   | Health-check da API                                  |

## Exemplo de requisição

**Criar item:**

```bash
curl -X POST http://127.0.0.1:8000/items \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Garrafa Térmica Aço",
    "category": "Casa",
    "price": 79.9,
    "stock": 25,
    "description": "Garrafa térmica de 750ml, mantém temperatura por 12h."
  }'
```

**Resposta:**

```json
{
  "id": 7,
  "name": "Garrafa Térmica Aço",
  "description": "Garrafa térmica de 750ml, mantém temperatura por 12h.",
  "category": "Casa",
  "price": 79.9,
  "stock": 25,
  "image_url": "https://picsum.photos/seed/garrafa-termica-aco/400/300"
}
```

## Próximos passos (ideias de evolução)

- Autenticação (JWT) para rotas de escrita
- Upload real de imagens (S3 ou storage local)
- Testes automatizados com `pytest` e `httpx`
- Deploy em Render/Railway com PostgreSQL

## Licença

MIT — sinta-se livre para usar este projeto como base para o seu próprio portfólio.
