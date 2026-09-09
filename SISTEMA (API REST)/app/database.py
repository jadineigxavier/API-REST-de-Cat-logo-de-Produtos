from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///./catalog.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def init_db() -> None:
    """Cria as tabelas no banco caso ainda não existam."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Dependência do FastAPI que fornece uma sessão de banco por requisição."""
    with Session(engine) as session:
        yield session
