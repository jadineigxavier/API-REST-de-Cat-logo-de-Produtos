from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from .. import crud, schemas
from ..database import get_session

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=List[schemas.ItemRead])
def read_items(
    category: Optional[str] = Query(None, description="Filtra itens por categoria"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, le=200),
    session: Session = Depends(get_session),
):
    """Lista os itens do catálogo, com filtro opcional por categoria e paginação."""
    return crud.list_items(session, category=category, skip=skip, limit=limit)


@router.get("/{item_id}", response_model=schemas.ItemRead)
def read_item(item_id: int, session: Session = Depends(get_session)):
    """Busca um item específico pelo id."""
    item = crud.get_item(session, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return item


@router.post("", response_model=schemas.ItemRead, status_code=201)
def create_item(item_in: schemas.ItemCreate, session: Session = Depends(get_session)):
    """Cria um novo item. Se image_url não for enviado, uma imagem genérica é gerada."""
    return crud.create_item(session, item_in)


@router.put("/{item_id}", response_model=schemas.ItemRead)
def update_item(
    item_id: int, item_in: schemas.ItemUpdate, session: Session = Depends(get_session)
):
    """Atualiza parcialmente um item existente."""
    item = crud.get_item(session, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return crud.update_item(session, item, item_in)


@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int, session: Session = Depends(get_session)):
    """Remove um item do catálogo."""
    item = crud.get_item(session, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    crud.delete_item(session, item)
