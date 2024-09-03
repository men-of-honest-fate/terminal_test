from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from .auth import oauth2_scheme
from api.models import base
from api.models import crud
from api.models.schemas import Create_Site, Get_Site, Update_Site


sites = APIRouter()


@sites.post("/create_site/")
def create_site(token: Annotated[str, Depends(oauth2_scheme)], site: Create_Site, db: Session = Depends(base.get_db)):
    db_site = crud.create_site(db=db, site=site)
    return {
        "info": Get_Site.model_validate(db_site.__dict__).model_dump(),
        "token": db_site.token,
    }


@sites.get("/get_sites/", response_model=list[Get_Site])
def get_sites(token: Annotated[str, Depends(oauth2_scheme)], skip: int = 0, limit: int = 100, db: Session = Depends(base.get_db)):
    sites = crud.get_sites(db, skip=skip, limit=limit)
    return (Get_Site.model_validate(i.__dict__).model_dump() for i in sites)


@sites.get("/get_site/", response_model=Get_Site)
def get_site(token: Annotated[str, Depends(oauth2_scheme)], id: int, db: Session = Depends(base.get_db)):
    site = crud.get_site(db, id=id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return Get_Site.model_validate(site.__dict__).model_dump()


@sites.delete("/delete_site", response_model=None)
def delete_site(token: Annotated[str, Depends(oauth2_scheme)], get_id: int, db: Session = Depends(base.get_db)):
    crud.delete_site(db, get_id=get_id)


@sites.patch("/update_site/", response_model=Get_Site)
def update_site(token: Annotated[str, Depends(oauth2_scheme)], id: int, site: Update_Site, db: Session = Depends(base.get_db)):
    db_site = crud.update_site(db, id=id, site=site)
    return Get_Site.model_validate(db_site.__dict__).model_dump()
