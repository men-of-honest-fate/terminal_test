from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from api.models.schemas import Create_Site, Create_Terminal, Get_Site, Get_Terminal, Update_Site, Update_Terminal
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models.db import Site
import models
from models.crud import create_site, create_terminal, get_site, get_terminal
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/create_site/", response_model=Create_Site)
def create_site1(site: Create_Site, db: Session = Depends(get_db)):
    db_site = create_site(db)
    if db_site:
        raise HTTPException(status_code=400, detail="Site happily created")
    return create_site(db=db, site=site)
#post запрос инфа нам, get пользователям 
@app.post("/create_terminal/", response_model=Create_Terminal)
def create_terminal1(terminal: Create_Terminal, db: Session = Depends(get_db)):
    db_terminal = create_terminal(db)
    if db_terminal:
        raise HTTPException(status_code=400, detail="Terminal happily created")
    return create_terminal(db=db, terminal=terminal)
@app.post("/get_site/", response_model=Get_Site)
def get_site1(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    site = get_site(db, skip=skip, limit=limit)
    return site
@app.post("/get_terminal/", response_model=Get_Site)
def get_terminal1(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    terminal = get_terminal(db, skip=skip, limit=limit)
    return terminal
