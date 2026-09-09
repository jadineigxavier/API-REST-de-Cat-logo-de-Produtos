from typing import Optional

from sqlmodel import Field, SQLModel


class Item(SQLModel, table=True):
    """Representa um item do catálogo persistido no banco de dados."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=120)
    description: Optional[str] = Field(default=None, max_length=500)
    category: str = Field(index=True, max_length=60)
    price: float
    stock: int = Field(default=0, ge=0)
    image_url: Optional[str] = None
