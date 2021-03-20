import datetime, uuid
import model as mdUser
from pg_db import database, users
from fastapi import FastAPI
from typing import List
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI(
    docs_url="/api/v2/docs",
    redoc_url="/api/v2/redocs",
    title="Core API",
    description="New Framework of Python",
    version="2.0",
    openapi_url="/api/v2/openapi.json",
    
)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/users", response_model=List[mdUser.UserList], tags=["Users"])
async def find_all_users():
    query = users.select()
    return await database.fetch_all(query)

@app.post("/users", response_model=mdUser.UserList, tags=["Users"])
async def register_user(user: mdUser.UserEntry):
    gID   = str(uuid.uuid1())
    gDate =str(datetime.datetime.now())
    query = users.insert().values(
        id = gID,
        username   = user.username,
        password   = pwd_context.hash(user.password),
        first_name = user.first_name,
        last_name  = user.last_name,
        gender     = user.gender,
        create_at  = gDate,
        status     = "1"
    ) 

    await database.execute(query)
    return {
        "id": gID,
        **user.dict(),
        "create_at":gDate,
        "status": "1"
    }

@app.get("/users/{userId}", response_model=mdUser.UserList, tags=["Users"])
async def find_user_by_id(userId: str):
    query = users.select().where(users.c.id == userId)
    return await database.fetch_one(query)

@app.put("/users", response_model=mdUser.UserList, tags=["Users"])
async def update_user(user: mdUser.UserUpdate):
    gDate = str(datetime.datetime.now())
    query = users.update().\
        where(users.c.id == user.id).\
        values(
            first_name = user.first_name,
            last_name  = user.last_name,
            gender     = user.gender,
            status     = user.status,
            create_at  = gDate,
        )
    await database.execute(query)

    return await find_user_by_id(user.id)

@app.delete("/users/{userId}", tags=["Users"])
async def delete_user(user: mdUser.UserDelete):
    query = users.delete().where(users.c.id == user.id)
    await database.execute(query)

    return {
        "status" : True,
        "message": "This user has been deleted successfully." 
    }

@app.get("/courses", tags=["Courses"])
def find_all_courses():
    return "List all courses."
    