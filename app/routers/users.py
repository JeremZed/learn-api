from fastapi import APIRouter, Depends, HTTPException, Request, Query
from fastapi.responses import JSONResponse

from app.dependencies import get_db, get_current_user, check_is_admin
from app.core.models import UserCurrent

from bson import ObjectId
from app.core.tools import clean_item

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[ Depends(get_current_user), Depends(check_is_admin)],
    responses={404: {"description": "Not found"}},
)

fake_users_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}


@router.get("/", name='admin.users.list')
async def read_users(
        request : Request,
        db = Depends(get_db),
        page: int = Query(1, ge=1),
        limit: int = Query(10, ge=1, le=100)
    ) -> JSONResponse:

    skip = (page - 1) * limit

    collection = db.get_collection("users")
    users = await collection.find().skip(skip).limit(limit).to_list(length=None)

    message = request.app.translator.get(request.state.current_lang, "admin_users_list_all")

    return JSONResponse(
        status_code=200,
        content={
            "message" : message,
            "data" : {
                "users": [ UserCurrent( **user).model_dump(exclude={"password"}) for user in users]},
                "pagination": {
                    "page": page,
                    "limit": limit
                }
            }
    )

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