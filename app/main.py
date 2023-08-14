from fastapi import FastAPI
from starlette import status
from app.databases.config import Config
from app.databases.connection import Session, engine_factory, get_session
from starlette.responses import JSONResponse

from app.services.user_verification import UserNotFound

app = FastAPI()

Session.configure(bind=engine_factory(Config))


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.exception_handler(UserNotFound)
async def forbidden_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"detail": "user was not found"})
