from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from api.models import base
from api.models import crud
from api.models.db import Site
from api.models.schemas import Create_Terminal, Get_Terminal, Update_Terminal
from settings import get_settings

settings = get_settings()
engine = create_engine(settings.DB_DSN)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
base.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


terminals = APIRouter()


# post запрос инфа нам, get пользователям
@terminals.post("/create_terminal/", response_model=Get_Terminal)
def create_terminal(terminal: Create_Terminal, db: Session = Depends(get_db)):
    db_terminal = crud.create_terminal(terminal=terminal, db=db)
    return Get_Terminal.model_validate(db_terminal.__dict__).model_dump()


@terminals.get("/get_terminals/", response_model=list[Get_Terminal])
def get_terminals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    terminals = crud.get_terminals(db, skip=skip, limit=limit)
    return (Get_Terminal.model_validate(i.__dict__).model_dump() for i in terminals)


@terminals.get("/get_terminal/", response_model=Get_Terminal)
def get_terminal(id: int, db: Session = Depends(get_db)):
    terminal = crud.get_terminal(db=db, id=id)
    if not terminal:
        raise HTTPException(status_code=404, detail="Terminal not found")
    return Get_Terminal.model_validate(terminal.__dict__).model_dump()


@terminals.delete("/delete_terminal", response_model=None)
def delete_terminal(get_id: int, db: Session = Depends(get_db)):
    crud.delete_terminal(db, get_id=get_id)
