from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from api.models import base
from api.models import crud
from api.models.schemas import Authorize_Input
from settings import get_settings

auth = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/authorize")

@auth.post("/authorize", response_model=str)
def authorize(auth_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(base.get_db)):
    resp = crud.authorization(db=db, authorize={"login": auth_data.username, "password": auth_data.password})
    return resp
