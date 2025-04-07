from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .controller import Controller
from .schemas import List, ListCreate, ListUpdate, Test, User, UserCreate, UserUpdate

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


# Lists
@app.post("/lists", response_model=List)
async def create_list(_list: ListCreate) -> List:
    return con.create_list(_list)


@app.get("/lists/{list_id}", response_model=List)
async def get_list(list_id: str) -> List:
    try:
        return con.get_list(list_id)
    except:
        raise HTTPException(status_code=404, detail="List not found")


@app.put("/lists/{list_id}", response_model=List)
async def update_list(list_id: str, _list: ListUpdate) -> List:
    try:
        return con.update_list(list_id, _list)
    except:
        raise HTTPException(status_code=404, detail="List not found")


@app.delete("/lists/{list_id}")
async def delete_list(list_id: str) -> dict:
    try:
        return con.delete_list(list_id)
    except:
        raise HTTPException(status_code=404, detail="List not found")
