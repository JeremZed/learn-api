from fastapi import APIRouter, Depends, HTTPException, Request

from app.dependencies import get_db, get_current_user

from app.core.models import User
from bson import ObjectId
from app.core.tools import clean_item

router = APIRouter(
    prefix="/users",
    tags=["users"],
    # dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}},
)

fake_users_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}


@router.get("/")
async def read_users():
    return fake_users_db

@router.put(
    "/{id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(id: str):
    if id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"id": id, "name": "The great Plumbus"}


@router.get("/{user_id}", name="user.get")
async def get_user(
    user_id: str,
    request:Request,
    db=Depends(get_db)
    ):

    collection = db.get_collection("users")

    user = clean_item(await collection.find_one({"_id": ObjectId(user_id)}))

    if user is None:
        message = request.app.translator.get(request.state.current_lang, "user_not_found")
        raise HTTPException(status_code=404, detail=message)

    return user