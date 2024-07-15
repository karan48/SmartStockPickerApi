from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def read_users():
    return [{"user_id": "user1"}, {"user_id": "user2"}]


@router.get("/{user_id}")
def read_user(user_id: str):
    return {"user_id": user_id}


@router.post("/")
def create_user(user: dict):
    return {"user_id": "new_user", "user": user}
