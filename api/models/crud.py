import hashlib
import secrets

from sqlalchemy.orm import Session

from api.models.db import Site, Terminal
from api.models.schemas import Create_Site, Create_Terminal, Authorize_Input

# def create_site(db: Session, ):
#     return db.query().filter(models.User.id == user_id).first()


# def get_user_by_email(db: Session, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()


# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()
# id: Mapped[int] = mapped_column(primary_key = True)
#     url: Mapped[str] = mapped_column(nullable = False)
#     bank_number: Mapped[str] = mapped_column(nullable = False)
#     login: Mapped[str] = mapped_column(nullable = False)
#     password: Mapped[str] = mapped_column(nullable = False)


#   id: Mapped[int] = mapped_column(primary_key = True)
#     limit_sum: Mapped[int] = mapped_column(nullable = False)
#     limit_req: Mapped[int] = mapped_column(nullable = False)


def create_site(db: Session, site: Create_Site):
    db_site = Site(
        url=site.url,
        bank_number=site.bank_number,
        login=site.login,
        password=site.password,
        token=secrets.token_hex(),
    )
    db.add(db_site)
    db.commit()
    db.refresh(db_site)
    return db_site


def create_terminal(db: Session, terminal: Create_Terminal):
    db_terminal = Terminal(
        limit_sum=terminal.limit_sum,
        limit_req=terminal.limit_req,
    )
    db.add(db_terminal)
    db.commit()
    db.refresh(db_terminal)
    return db_terminal


def update_site(
    db: Session,
    site: Create_Site,
):
    pass


def get_sites(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Site).offset(skip).limit(limit).all()


def get_site(db: Session, id: int):
    return db.query(Site).filter(Site.id == id).one_or_none()


# в ручке гет превратить в модели пайдантик уже в самой ручке
def get_terminals(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Terminal).offset(skip).limit(limit).all()


def get_terminal(db: Session, id: int):
    return db.query(Terminal).filter(Terminal.id == id).one_or_none()


# в ручке гет превратить в модели пайдантик уже в самой ручке
def delete_site(db: Session, get_id: int):
    obj = db.query(Site).filter(Site.id == get_id).one_or_none()
    if obj:
        db.delete(obj)
        db.commit()


def delete_terminal(db: Session, get_id: int):
    obj = db.query(Terminal).filter(Terminal.id == get_id).one_or_none()
    if obj:
        db.delete(obj)
        db.commit()


def authorization(db: Session, authorize: Authorize_Input):
    user = (
        db.query(Site)
        .filter(
            Site.login == authorize.login,
            Site.password == authorize.password,
        )
        .one_or_none()
    )
    if user:
        new_token = secrets.token_hex()
        user.token = new_token
        db.commit()
        return new_token
