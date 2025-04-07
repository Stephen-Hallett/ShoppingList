from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .controller import Controller
from .schemas import (
    Item,
    ItemCreate,
    ItemUpdate,
    ShoppingList,
    ShoppingListCreate,
    ShoppingListUpdate,
    Test,
    User,
    UserCreate,
    UserUpdate,
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

con = Controller()


@app.get("/test")
async def test() -> Test:
    return con.test()


@app.post("/users", response_model=User)
async def create_user(user: UserCreate) -> User:
    return con.create_user(user)


@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: str) -> User:
    try:
        return con.get_user(user_id)
    except:
        raise HTTPException(status_code=404, detail="User not found")


@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: str, user: UserUpdate) -> User:
    try:
        return con.update_user(user_id, user)
    except:
        raise HTTPException(status_code=404, detail="User not found")


@app.delete("/users/{user_id}")
async def delete_user(user_id: str) -> dict:
    try:
        return con.delete_user(user_id)
    except:
        raise HTTPException(status_code=404, detail="User not found")


# ShoppingLists
@app.post("/shoppinglists", response_model=ShoppingList)
async def create_shoppinglist(shoppinglist: ShoppingListCreate) -> ShoppingList:
    return con.create_shoppinglist(shoppinglist)


@app.get("/shoppinglists/{shoppinglist_id}", response_model=ShoppingList)
async def get_shoppinglist(shoppinglist_id: str) -> ShoppingList:
    try:
        return con.get_shoppinglist(shoppinglist_id)
    except:
        raise HTTPException(status_code=404, detail="ShoppingList not found")


@app.put("/shoppinglists/{shoppinglist_id}", response_model=ShoppingList)
async def update_shoppinglist(
    shoppinglist_id: str, shoppinglist: ShoppingListUpdate
) -> ShoppingList:
    try:
        return con.update_shoppinglist(shoppinglist_id, shoppinglist)
    except:
        raise HTTPException(status_code=404, detail="ShoppingList not found")


@app.delete("/shoppinglists/{shoppinglist_id}")
async def delete_shoppinglist(shoppinglist_id: str) -> dict:
    try:
        return con.delete_shoppinglist(shoppinglist_id)
    except:
        raise HTTPException(status_code=404, detail="ShoppingList not found")


@app.post("/items", response_model=Item)
async def create_item(item: ItemCreate) -> Item:
    return con.create_item(item)


@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: str) -> Item:
    try:
        return con.get_item(item_id)
    except:
        raise HTTPException(status_code=404, detail="Item not found")


@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: ItemUpdate) -> Item:
    try:
        return con.update_item(item_id, item)
    except:
        raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/items/{item_id}")
async def delete_item(item_id: str) -> dict:
    try:
        return con.delete_item(item_id)
    except:
        raise HTTPException(status_code=404, detail="Item not found")
