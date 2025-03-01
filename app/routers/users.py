from fastapi import APIRouter, Depends, HTTPException, Request, Query
from fastapi.responses import JSONResponse

from app.dependencies import get_db, get_current_user, check_is_admin
from app.core.models import UserCurrent, User
from app.repo.user import UserRepository

from bson import ObjectId
from app.core.tools import clean_item, get_message, hash_password, generate_random_str
from datetime import datetime, timezone



async def check_email_already_user(email, collection, request):

    existing_user = await collection.find_one({"email": email})
    if existing_user:
        message = get_message(request, "admin_users_email_already_exist")
        raise HTTPException( status_code=400, detail=message )

    return False

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[ Depends(get_current_user), Depends(check_is_admin)],
    responses={404: {"description": "Not found"}},
)

@router.get("/", name='admin.users.list')
async def read_users(
        request : Request,
        db = Depends(get_db),
        page: int = Query(1, ge=1),
        limit: int = Query(10, ge=1, le=100)
    ) -> JSONResponse:

    """
        Route qui permet de lister tous les utilisateurs
    """

    repo = UserRepository(db)
    users = await repo.get_all_users(skip=(page - 1) * limit, limit=limit)

    message = get_message(request, "admin_users_list_all")

    return JSONResponse(
        status_code=200,
        content={
            "message" : message,
            "data" : {
                "users": [ User( **clean_item(user)).model_dump() for user in users]},
                "pagination": {
                    "page": page,
                    "limit": limit
                }
            }
    )

@router.put("/{id}", name='admin.users.update')
async def update_user(
        request: Request,
        id:str,
        data : User,
        db=Depends(get_db)
    ) -> JSONResponse:

    """
        Route qui permet de modifier un utilisateur
    """

    repo = UserRepository(db)
    existing_user = await repo.get_user_by_id(id)

    if not existing_user:
        message = get_message(request, "admin_users_not_found")
        raise HTTPException( status_code=404, detail=message )

    update_fields = {k: v for k, v in data.model_dump(exclude_unset=True, exclude=['id']).items()}

    if 'email' in update_fields and update_fields['email'] != existing_user['email']:
        if await repo.check_email_exists(update_fields['email']):
            raise HTTPException(status_code=400, detail=get_message(request, "admin_users_email_already_exist"))

    await repo.update_user(id, update_fields)

    message = get_message(request, "admin_users_updated")
    return JSONResponse( status_code=200,  content={"message": message})

@router.get("/{id}", name="admin.user.get")
async def get_user(
        id: str,
        request:Request,
        db=Depends(get_db)
    ) -> JSONResponse:

    """
        Route qui permet de retourner les informations d'un utilisateur
    """

    repo = UserRepository(db)
    user = clean_item(await repo.get_user_by_id(id), exclude=['password'])

    if user is None:
        message = get_message(request, "user_not_found")
        raise HTTPException(status_code=404, detail=message)

    return JSONResponse( status_code=200,  content={"user": user})

@router.post("/", name="admin.user.create")
async def create_user(
    request : Request,
    data : User,
    db=Depends(get_db)
    ) -> JSONResponse:

    """
        Route qui permet de créer un nouvel utilisateur avec un mot de passe automatique
    """
    repo = UserRepository(db)

    if await repo.check_email_exists(data.email):
        raise HTTPException(status_code=400, detail=get_message(request, "admin_users_email_already_exist"))


    user_data = data.model_dump(exclude_unset=True)
    user_data["password"] = generate_random_str()
    await repo.create_user(user_data)

    message = get_message(request, "admin_user_created")

    return JSONResponse( status_code=200,  content={"message": message})

@router.delete("/{id}", name="admin.user.remove")
async def remove_user(
    request : Request,
    id : str,
    db=Depends(get_db)
    ) ->JSONResponse:

    repo = UserRepository(db)
    user = await repo.get_user_by_id(id)

    if user is None:
        message = get_message(request, "user_not_found")
        raise HTTPException(status_code=404, detail=message)

    # delete_result = await collection.delete_one({"_id": ObjectId(id)})

    await repo.soft_delete_user(id)

    message = get_message(request, "admin_user_deleted")

    return JSONResponse(status_code=200, content={"message" : message})