from fastapi import  HTTPException, Depends
from app.dependencies import get_current_user, check_is_admin
from app.core.models import  User
from app.core.forms.admin import FormRegister
from app.repo.user import UserRepository
from app.core.tools import get_message, clean_item, hash_password
from app.routers.base_router import create_crud_routes


# DEFINTION DES HOOKS

async def before_create_user(repo, form, request):
    """
    On checke si un email existe déjà avant création
    """
    if await repo.check_email_exists(form.email):
        raise HTTPException(status_code=400, detail=get_message(request, "admin_users_email_already_exist"))

    form.password = hash_password(form.password)

async def after_create_user(repo, new_user, request):
    """
    Après la création en base on effectue une action...
    """
    print(f"Email envoyé à {new_user['email']}")

async def before_delete_user(repo, user_id, request):
    """
        On interdit la suppression de l'utilisateur admin
    """
    user = await repo.get_by_id(user_id)
    if user and user.get("role") == "admin":
        raise HTTPException(status_code=403, detail=get_message(request, "admin_users_delete_admin"))

async def after_read_all(repo, items, request):
    """
        Après avoir récupérer tous les items
    """

    items = [ clean_item(item, model=User, exclude=['password']) for item in items]

async def after_read_one(repo, item, request):
    """
        Après avoir récupéré l'item
    """

    item = clean_item(item, model=User, exclude=['password'])

##########################

hooks = {
    "before_create": before_create_user,
    "after_create": after_create_user,
    "before_delete": before_delete_user,
    "after_read_all" : after_read_all,
    "after_read_one" : after_read_one,
}

forms = {
    "create" : FormRegister
}

dependencies=[
    Depends(get_current_user),
    Depends(check_is_admin)
]

router = create_crud_routes(
    "users",
    UserRepository,
    User,
    hooks=hooks,
    forms=forms,
    dependencies=dependencies
)


# router = APIRouter(
#     prefix="/users",
#     tags=["users"],
#     dependencies=[ Depends(get_current_user), Depends(check_is_admin)],
#     responses={404: {"description": "Not found"}},
# )

# @router.get("/", name='admin.users.list')
# async def read_users(
#         request : Request,
#         db = Depends(get_db),
#         page: int = Query(1, ge=1),
#         limit: int = Query(10, ge=1, le=100)
#     ) -> JSONResponse:

#     """
#         Route qui permet de lister tous les utilisateurs
#     """

#     repo = UserRepository(db)
#     users = await repo.get_all(skip=(page - 1) * limit, limit=limit)

#     message = get_message(request, "admin_users_list_all")

#     return JSONResponse(
#         status_code=200,
#         content={
#             "message" : message,
#             "data" : {
#                 "users": [ User( **clean_item(user)).model_dump() for user in users]},
#                 "pagination": {
#                     "page": page,
#                     "limit": limit
#                 }
#             }
#     )

# @router.put("/{id}", name='admin.users.update')
# async def update_user(
#         request: Request,
#         id:str,
#         data : User,
#         db=Depends(get_db)
#     ) -> JSONResponse:

#     """
#         Route qui permet de modifier un utilisateur
#     """

#     repo = UserRepository(db)
#     existing_user = await repo.get_by_id(id)

#     if not existing_user:
#         message = get_message(request, "admin_users_not_found")
#         raise HTTPException( status_code=404, detail=message )

#     update_fields = {k: v for k, v in data.model_dump(exclude_unset=True, exclude=['id']).items()}

#     if 'email' in update_fields and update_fields['email'] != existing_user['email']:
#         if await repo.check_email_exists(update_fields['email']):
#             raise HTTPException(status_code=400, detail=get_message(request, "admin_users_email_already_exist"))

#     await repo.update(id, update_fields)

#     message = get_message(request, "admin_users_updated")
#     return JSONResponse( status_code=200,  content={"message": message})

# @router.get("/{id}", name="admin.user.get")
# async def get_user(
#         id: str,
#         request:Request,
#         db=Depends(get_db)
#     ) -> JSONResponse:

#     """
#         Route qui permet de retourner les informations d'un utilisateur
#     """

#     repo = UserRepository(db)
#     user = clean_item(await repo.get_by_id(id), exclude=['password'])

#     if user is None:
#         message = get_message(request, "user_not_found")
#         raise HTTPException(status_code=404, detail=message)

#     return JSONResponse( status_code=200,  content={"user": user})

# @router.post("/", name="admin.user.create")
# async def create_user(
#     request : Request,
#     data : User,
#     db=Depends(get_db)
#     ) -> JSONResponse:

#     """
#         Route qui permet de créer un nouvel utilisateur avec un mot de passe automatique
#     """
#     repo = UserRepository(db)

#     if await repo.check_email_exists(data.email):
#         raise HTTPException(status_code=400, detail=get_message(request, "admin_users_email_already_exist"))


#     user_data = data.model_dump(exclude_unset=True)
#     user_data["password"] = generate_random_str()
#     await repo.create(user_data)

#     message = get_message(request, "admin_user_created")

#     return JSONResponse( status_code=200,  content={"message": message})

# @router.delete("/{id}", name="admin.user.remove")
# async def remove_user(
#     request : Request,
#     id : str,
#     db=Depends(get_db)
#     ) ->JSONResponse:

#     repo = UserRepository(db)
#     user = await repo.get_by_id(id)

#     if user is None:
#         message = get_message(request, "user_not_found")
#         raise HTTPException(status_code=404, detail=message)

#     # delete_result = await collection.delete_one({"_id": ObjectId(id)})

#     await repo.soft_delete(id)

#     message = get_message(request, "admin_user_deleted")

#     return JSONResponse(status_code=200, content={"message" : message})