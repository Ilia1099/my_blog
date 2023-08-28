from fastapi import FastAPI
from app.databases.config import Config
from app.databases.connection import Session, engine_factory, get_session
from starlette.responses import JSONResponse
from app.api.routes import users
# from app.services.user_verification import UserNotFound

eng = engine_factory(Config)
Session.configure(bind=eng)
app = FastAPI()

app.include_router(users.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


# @app.exception_handler(UserNotFound)
# async def forbidden_exception_handler(request, exc):
#     return JSONResponse(status_code=exc.status_code, content={"detail": "user was not found"})
