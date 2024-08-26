from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from api.models.schemas import Create_Site, Create_Terminal, Get_Site, Get_Terminal, Update_Site, Update_Terminal
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models.db import Site
import models
from models.crud import create_site, create_terminal, get_site, get_terminal, delete_site
from base import get_db 
app = FastAPI()

@app.post("/create_site/", response_model=Create_Site)
def create_site1(site: Create_Site, db: Session = Depends(get_db)):
    db_site = create_site(db = db, site = site)
    return Create_Site.model_validate(db_site).model_dump()
#post запрос инфа нам, get пользователям 
@app.post("/create_terminal/", response_model=Create_Terminal)
def create_terminal1(terminal: Create_Terminal, db: Session = Depends(get_db)):
    db_terminal = create_terminal(db)
    return Create_Terminal.model_validate(db_terminal).model_dump()

@app.post("/get_site/", response_model=Get_Site)
def get_site1(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sites = get_site(db, skip=skip, limit=limit)
    return (Get_Site.model_validate(i).model_dump() for i in sites)
@app.post("/get_terminal/", response_model=Get_Site)
def get_terminal1(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    terminals = get_terminal(db, skip=skip, limit=limit)
    return (Get_Terminal.model_validate(i).model_dump() for i in terminals)
@app.post("/delete_site", response_model = None)
def delete_site1(get_id: int, db: Session = Depends(get_db)):
    delete_site(db, get_id=get_id)
@app.post("/delete_terminal", response_model = None)
def delete_terminal1(get_id: int, db: Session = Depends(get_db)):
    delete_site(db, get_id=get_id)

