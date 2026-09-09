from typing import Optional

from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=120, examples=["Cadeira Escritório Confort"])
    description: Optional[str] = Field(None, max_length=500)
    category: str = Field(..., min_length=1, max_length=60, examples=["Móveis"])
    price: float = Field(..., gt=0, examples=[459.9])
    stock: int = Field(0, ge=0, examples=[12])
    image_url: Optional[str] = Field(
        None,
        description="Se não for informado, uma imagem genérica é gerada automaticamente.",
    )


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    """Todos os campos são opcionais: só o que for enviado é atualizado."""

    name: Optional[str] = Field(None, min_length=1, max_length=120)
    description: Optional[str] = Field(None, max_length=500)
    category: Optional[str] = Field(None, min_length=1, max_length=60)
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    image_url: Optional[str] = None


class ItemRead(ItemBase):
    id: int
