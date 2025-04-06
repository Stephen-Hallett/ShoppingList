from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .controller import Controller
from .schemas import Test, User, UserCreate, UserUpdate

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
