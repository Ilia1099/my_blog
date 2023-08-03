from fastapi import FastAPI
from starlette import status
from starlette.responses import JSONResponse

from services.user_verification import UserNotFound

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.exception_handler(UserNotFound)
async def forbidden_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"detail": "user was not found"})
