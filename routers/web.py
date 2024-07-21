from fastapi import APIRouter, Request, Form, Depends, Cookie
from sqlmodel import Session
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from db import get_session
from routers.cars import get_cars


routers = APIRouter()

templates = Jinja2Templates(directory="templates")


@routers.get("/", response_class=HTMLResponse)
def home(request: Request, cars_cookie: str | None = Cookie(None)):
    print(cars_cookie)
    return templates.TemplateResponse("home.html",
                                      {"request": request})


@routers.post("/search", response_class=HTMLResponse)
def search(*, size: str = Form(...), doors: int = Form(...),
           request: Request,
           session: Session = Depends(get_session)):
    car = get_cars(size=size, doors=doors, session=session)
    return templates.TemplateResponse("search_result.html",
                                      {"request": request, "cars": car})
