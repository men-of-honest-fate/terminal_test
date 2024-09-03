from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from api import __version__
from api.models import base
from settings import get_settings

from .root import root
from .sites import sites
from .websockets import ws
from .terminals import terminals
from .auth import auth

settings = get_settings()
app = FastAPI(
    title="Terminal API",
    description="An API for terminal automation",
    version=__version__,
    # Отключаем нелокальную документацию
    root_path=settings.ROOT_PATH if __version__ != "dev" else "",
    docs_url="/" if __version__ != "dev" else "/docs",
    redoc_url=None,
)


app.add_middleware(
    DBSessionMiddleware,
    db_url=str(settings.DB_DSN),
    engine_args={"pool_pre_ping": True, "isolation_level": "AUTOCOMMIT"},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

app.include_router(root, prefix="", tags=["root"])
app.include_router(ws, prefix="/ws", tags=["Websockets"])
app.include_router(sites, prefix="/sites", tags=["Sites"])
app.include_router(terminals, prefix="/terminals", tags=["Terminals"])
app.include_router(auth, prefix="/auth", tags=["Auth"])
