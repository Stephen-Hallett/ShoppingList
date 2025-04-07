from pydantic import BaseModel, EmailStr


class Test(BaseModel):
    test: str


class User(BaseModel):
    id: str  # will be RowKey
    email: EmailStr
    name: str


class UserCreate(BaseModel):
    email: EmailStr
    name: str


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    name: str | None = None


class List(BaseModel):
    id: str  # will be RowKey
    name: str


class ListCreate(BaseModel):
    name: str


class ListUpdate(BaseModel):
    name: str | None = None
