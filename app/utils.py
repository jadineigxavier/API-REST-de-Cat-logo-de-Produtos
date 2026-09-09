import re


def placeholder_image(seed_text: str, width: int = 400, height: int = 300) -> str:
    """Gera a URL de uma imagem genérica e determinística (o mesmo nome
    sempre produz a mesma imagem), útil para preencher o catálogo com
    fotos de exemplo sem precisar hospedar arquivos reais.
    """
    slug = re.sub(r"[^a-z0-9]+", "-", seed_text.lower()).strip("-") or "item"
    return f"https://picsum.photos/seed/{slug}/{width}/{height}"
