from fastapi import FastAPI
from app.databases.config import Config
from app.databases.connection import Session, engine_factory
from app.api.routes import users, posts

eng = engine_factory(Config)
Session.configure(bind=eng)


app = FastAPI()

app.include_router(users.router)
app.include_router(posts.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
