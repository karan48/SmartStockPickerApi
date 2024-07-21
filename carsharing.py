from fastapi import FastAPI, Request
import uvicorn
from sqlmodel import SQLModel
from fastapi.middleware.cors import CORSMiddleware

from db import engine
from routers import cars, web, auth

app = FastAPI(title="Car Sharing")
app.include_router(web.routers)
app.include_router(cars.router)

origins = [
    "http://localhost:8000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


@app.middleware("http")
async def add_car_cookies(request: Request, call_next):
    response = await call_next(request)
    response.set_cookie(key="cars_cookie", value="you_visited_the_carsharing_app")
    return response


if __name__ == "__main__":
    uvicorn.run("carsharing:app", reload=True, port=8001)
