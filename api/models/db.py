import sqlalchemy as sa
from sqlalchemy import Column
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

from .base import Base


# site:
# id - int
# url - str
# bank_number: str
# login: str
# password: str
class Site(Base):
    __tablename__ = "site"
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(nullable=False, unique=True)
    bank_number: Mapped[str] = mapped_column(nullable=False, unique=True)
    login: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False, unique=True)
    token: Mapped[str] = mapped_column(unique=True)


# terminal:
# id - int
# limit_sum: int
# limit_req: int
class Terminal(Base):
    __tablename__ = "terminal"
    id: Mapped[int] = mapped_column(primary_key=True)
    limit_sum: Mapped[int] = mapped_column(nullable=False)
    limit_req: Mapped[int] = mapped_column(nullable=False)
