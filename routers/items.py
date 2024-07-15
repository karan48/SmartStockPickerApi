from fastapi import APIRouter

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def read_items():
    return [{"item_id": "item1"}, {"item_id": "item2"}]


@router.get("/{item_id}")
def read_item(item_id: str):
    return {"item_id": item_id}


@router.post("/")
def create_item(item: dict):
    return {"item_id": "new_item", "item": item}
