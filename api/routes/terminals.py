from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from .auth import oauth2_scheme
from typing import Annotated
from api.models import base
from api.models import crud
from api.models.db import Site
from api.models.schemas import Create_Terminal, Get_Terminal, Update_Terminal
from settings import get_settings

terminals = APIRouter()


# post запрос инфа нам, get пользователям
@terminals.post("/create_terminal/", response_model=Get_Terminal)
def create_terminal(token: Annotated[str, Depends(oauth2_scheme)], terminal: Create_Terminal, db: Session = Depends(base.get_db)):
    db_terminal = crud.create_terminal(terminal=terminal, db=db)
    return Get_Terminal.model_validate(db_terminal.__dict__).model_dump()


@terminals.get("/get_terminals/", response_model=list[Get_Terminal])
def get_terminals(token: Annotated[str, Depends(oauth2_scheme)], skip: int = 0, limit: int = 100, db: Session = Depends(base.get_db)):
    terminals = crud.get_terminals(db, skip=skip, limit=limit)
    return (Get_Terminal.model_validate(i.__dict__).model_dump() for i in terminals)


@terminals.get("/get_terminal/", response_model=Get_Terminal)
def get_terminal(token: Annotated[str, Depends(oauth2_scheme)], params: Request, db: Session = Depends(base.get_db)):
    terminal = crud.get_terminal(db=db, params=params)
    if not terminal:
        raise HTTPException(status_code=404, detail="Terminal not found")
    return Get_Terminal.model_validate(terminal.__dict__).model_dump()


@terminals.delete("/delete_terminal", response_model=None)
def delete_terminal(token: Annotated[str, Depends(oauth2_scheme)], get_id: int, db: Session = Depends(base.get_db)):
    crud.delete_terminal(db, get_id=get_id)


@terminals.patch("/update_site/", response_model=Get_Terminal)
def update_site(token: Annotated[str, Depends(oauth2_scheme)], id: int, terminal: Update_Terminal, db: Session = Depends(base.get_db)):
    db_site = crud.update_terminal(db, id=id, terminal=terminal)
    return Get_Terminal.model_validate(db_site.__dict__).model_dump()

# @terminals.post("/payment/", response_model=None)
# def payment(token: Annotated[str, Depends(oauth2_scheme)], terminal: Update_Terminal, db: Session = Depends(base.get_db))::
    
