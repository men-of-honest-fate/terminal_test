from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from api.models import base
from api.models import crud
from api.models.schemas import Authorize_Input, Authorize_Response
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


auth = APIRouter()


@auth.post("/authorize", response_model=Authorize_Response)
def authorize(auth_data: Authorize_Input, db: Session = Depends(get_db)):
    resp = crud.authorization(db, authorize=auth_data)
    return Authorize_Response.model_validate(resp.__dict__).model_dump()
