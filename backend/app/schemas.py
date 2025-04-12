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
    name: str | None = None


class Item(BaseModel):
    id: str  # will be RowKey
    name: str


class ItemCreate(BaseModel):
    name: str


class ShoppingList(BaseModel):
    id: str  # will be RowKey
    name: str
    owner: str
    members: list = []
    items: list = []


class ShoppingListCreate(BaseModel):
    name: str
    owner: str
    members: list = []
    items: list = []


class ShoppingListUpdate(BaseModel):
    members: list | None = None
    items: list | None = None

class EmailRequest(BaseModel):
    email: EmailStr

class ItemName(BaseModel):
    item: str