import json

from pydantic import BaseModel, EmailStr, ValidationInfo


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


class Item(BaseModel):
    id: str  # will be RowKey
    name: str


class ItemCreate(BaseModel):
    name: str


class ItemUpdate(BaseModel):
    name: str


class JsonShoppingListStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: str = "[]", _: ValidationInfo = None) -> list:
        if not isinstance(v, str):
            raise TypeError("string required")

        try:
            loaded = json.loads(v)
        except json.JSONDecodeError:
            raise ValueError("string is not valid JSON")

        if not isinstance(loaded, list):
            raise ValueError("JSON string must decode to a list")

        if not all(isinstance(i, str) for i in loaded):
            raise ValueError("All items in the list must be strings (item IDs)")

        return cls(v)


class ShoppingList(BaseModel):
    id: str  # will be RowKey
    name: str
    items: JsonShoppingListStr = "[]"


class ShoppingListCreate(BaseModel):
    name: str
    items: JsonShoppingListStr = "[]"


class ShoppingListUpdate(BaseModel):
    name: str | None = None
    items: JsonShoppingListStr | None = None
