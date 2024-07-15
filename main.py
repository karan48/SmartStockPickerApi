import uvicorn
from fastapi import FastAPI
import routers.items as items
import routers.users as users

app = FastAPI()

app.include_router(items.router)
app.include_router(users.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI app!"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
