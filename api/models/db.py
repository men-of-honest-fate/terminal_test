import sqlalchemy as sa
from sqlalchemy import Column
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Mapped, mapped_column
# site:
# id - int
# url - str
# bank_number: str
# login: str
# password: str
class Base(declarative_base):
    pass
class Site(Base):
    __tablename__ = "site"
    id: Mapped[int] = mapped_column(primary_key = True)
    url: Mapped[str] = mapped_column(nullable = False)
    bank_number: Mapped[str] = mapped_column(nulable = False)
    login: Mapped[str] = mapped_column(nullable = False)
    password: Mapped[str] = mapped_column(nullable = False)

# terminal:
# id - int
# limit_sum: int
# limit_req: int
class Terminal(Base):
    __tablename__= "terminal"
    id: Mapped[int] = mapped_column(primary_key = True)
    limit_sum: Mapped[int] = mapped_column(nullable = False)
    limit_req: Mapped[int] = mapped_column(nullable = False)