from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from api.models import base
from api.models import crud
from api.models.schemas import Create_Site, Get_Site
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


sites = APIRouter()


@sites.post("/create_site/")
def create_site(site: Create_Site, db: Session = Depends(get_db)):
    db_site = crud.create_site(db=db, site=site)
    return {
        "info": Get_Site.model_validate(db_site.__dict__).model_dump(),
        "token": db_site.token,
    }


@sites.get("/get_sites/", response_model=list[Get_Site])
def get_sites(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sites = crud.get_sites(db, skip=skip, limit=limit)
    return (Get_Site.model_validate(i.__dict__).model_dump() for i in sites)


@sites.get("/get_site/", response_model=Get_Site)
def get_site(id: int, db: Session = Depends(get_db)):
    site = crud.get_site(db, id=id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return Get_Site.model_validate(site.__dict__).model_dump()


@sites.delete("/delete_site", response_model=None)
def delete_site(get_id: int, db: Session = Depends(get_db)):
    crud.delete_site(db, get_id=get_id)
