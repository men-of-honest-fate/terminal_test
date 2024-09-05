from pydantic import BaseModel, Field
from typing import Optional

class Create_Site(BaseModel):
    url: str
    bank_number: str
    login: str
    password: str


class Get_Site(BaseModel):
    id: int
    url: str
    bank_number: str
    login: str


class Update_Site(BaseModel):
    url: str | None = Field(default=None)
    bank_number: str | None = Field(default=None)
    login: str | None = Field(default=None)
    password: str | None = Field(default=None)


class Create_Terminal(BaseModel):
    limit_sum: int
    limit_req: int


class Get_Terminal(BaseModel):
    id: Optional[int] =  None
    limit_sum: Optional[int] =  None
    limit_req: Optional[int] =  None


class Update_Terminal(BaseModel):
    limit_sum: int | None = Field(default=None)
    limit_req: int | None = Field(default=None)


class Authorize_Input(BaseModel):
    login: str
    password: str

# _tablename__ = "site"
#     id: Mapped[int] = mapped_column(primary_key = True)
#     url: Mapped[str] = mapped_column(nullable = False)
#     bank_number: Mapped[str] = mapped_column(nullable = False)
#     login: Mapped[str] = mapped_column(nullable = False)
#     password: Mapped[str] = mapped_column(nullable = False)
# __tablename__= "terminal"
#     id: Mapped[int] = mapped_column(primary_key = True)
#     limit_sum: Mapped[int] = mapped_column(nullable = False)
#     limit_req: Mapped[int] = mapped_column(nullable = False)
