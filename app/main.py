from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select

from . import models
from .database import engine, init_db
from .routers import items
from .utils import placeholder_image

STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI(
    title="Catalog API",
    description=(
        "API simples para consulta e gerenciamento de itens de um catálogo. "
        "Itens sem imagem definida recebem automaticamente uma imagem genérica."
    ),
    version="1.0.0",
)

app.include_router(items.router)


SEED_ITEMS = [
    {
        "name": "Cadeira Escritório Confort",
        "category": "Móveis",
        "price": 459.9,
        "stock": 12,
        "description": "Cadeira ergonômica com apoio de braço ajustável.",
    },
    {
        "name": "Fone Bluetooth Aria",
        "category": "Eletrônicos",
        "price": 189.0,
        "stock": 30,
        "description": "Fone sem fio com cancelamento de ruído.",
    },
    {
        "name": "Caneca Cerâmica Nórdica",
        "category": "Casa",
        "price": 39.9,
        "stock": 50,
        "description": "Caneca de 300ml em cerâmica fosca.",
    },
    {
        "name": "Mochila Urbana Trek",
        "category": "Acessórios",
        "price": 219.5,
        "stock": 18,
        "description": "Mochila resistente à água com compartimento para notebook.",
    },
    {
        "name": "Luminária de Mesa Lumen",
        "category": "Casa",
        "price": 129.0,
        "stock": 22,
        "description": "Luminária LED com regulagem de intensidade.",
    },
    {
        "name": "Teclado Mecânico Vortex",
        "category": "Eletrônicos",
        "price": 349.0,
        "stock": 15,
        "description": "Teclado mecânico compacto com switches táteis.",
    },
]


def _seed_if_empty() -> None:
    with Session(engine) as session:
        if session.exec(select(models.Item)).first():
            return
        for data in SEED_ITEMS:
            data = {**data, "image_url": placeholder_image(data["name"])}
            session.add(models.Item(**data))
        session.commit()


@app.on_event("startup")
def on_startup() -> None:
    init_db()
    _seed_if_empty()


@app.get("/api/health", tags=["health"])
def health():
    return {"status": "ok", "docs": "/docs"}


# Serve a interface web (HTML/CSS/JS) na raiz do site.
# Precisa ser montado por último para não sobrepor as rotas da API acima.
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="frontend")
