import pytest
from models.crud import create_site, create_terminal
from sqlalchemy import create_engine, sessionmaker

from settings import get_settings


@pytest.fixture(scope="Session", autouse=True)
def db_connect():
    settings = get_settings()
    DB_URL = settings.DB_DSN
    engine = create_engine("postgresql://postgres:12345@localhost:5432/postgres")
