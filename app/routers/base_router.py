from typing import Optional, Callable, Dict
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse

from app.core.tools import get_message, clean_item
from app.dependencies import get_db

HooksType = Dict[str, Optional[Callable]]
FormsType = Dict[str, Optional[Callable]]

def create_crud_routes(
    entity_name: str,
    repo_class: type,
    model_class: type,
    prefix: str = 'admin',
    hooks: Optional[HooksType] = None,
    forms: Optional[FormsType] = None,
    dependencies: list = [],
    soft_delete = True
) -> APIRouter:

    if 'create' not in forms:
        forms['create'] = None

    if 'update' not in forms:
        forms['update'] = None

    router = APIRouter(prefix=f"/{entity_name}", tags=[entity_name], dependencies=dependencies)

    async def execute_hook(hook_name: str, *args):
        """
        Permet d'exécuter un hook s'il est défini
        """
        if hooks and hook_name in hooks and hooks[hook_name]:
            return await hooks[hook_name](*args)

    @router.get("/", name=f"{prefix}.{entity_name}.list")
    async def read_items(request: Request, db=Depends(get_db), page: int = 1, limit: int = 10):
        repo = repo_class(db)

        await execute_hook("before_read_all", repo, request)

        items = await repo.get_all(skip=(page - 1) * limit, limit=limit)
        message = get_message(request, f"{prefix}_{entity_name}_list")

        await execute_hook("after_read_all", repo, items, request)

        return JSONResponse(status_code=200, content={"message": message, "data": items})

    @router.get("/{id}", name=f"{prefix}.{entity_name}.get")
    async def get_item(id: str, request: Request, db=Depends(get_db)):
        repo = repo_class(db)

        await execute_hook("before_read_one", repo, id, request)

        item = await repo.get_by_id(id)
        if item is None:
            raise HTTPException(status_code=404, detail="Not found")

        await execute_hook("after_read_one", repo, item, request)

        return JSONResponse(status_code=200, content={"data": item})

    @router.post("/", name=f"{prefix}.{entity_name}.create")
    async def create_item(
        request: Request,
        form : forms['create'],
        db=Depends(get_db)
        ):

        repo = repo_class(db)

        await execute_hook("before_create", repo, form, request)

        item_data = form.model_dump()

        result = await repo.create(item_data)
        new_item = await repo.get_by_id(result.inserted_id)

        await execute_hook("after_create", repo, new_item, request)

        message = get_message(request, f"{prefix}_{entity_name}_created")
        return JSONResponse(status_code=201, content={"message": message})

    @router.put("/{id}", name=f"{prefix}.{entity_name}.update")
    async def update_item(id: str, request: Request, data: model_class, db=Depends(get_db)):
        repo = repo_class(db)

        await execute_hook("before_update", repo, id, data, request)

        update_data = data.model_dump(exclude_unset=True)
        await repo.update(id, update_data)

        await execute_hook("after_update", repo, id, request)

        message = get_message(request, f"{prefix}_{entity_name}_updated")
        return JSONResponse(status_code=200, content={"message": message})

    @router.delete("/{id}", name=f"{prefix}.{entity_name}.delete")
    async def delete_item(id: str, request: Request, db=Depends(get_db)):
        repo = repo_class(db)

        await execute_hook("before_delete", repo, id, request)

        if soft_delete:
            await repo.soft_delete(id)
        else:
            await repo.hard_delete(id)

        await execute_hook("after_delete", repo, id, request)

        message = get_message(request, f"{prefix}_{entity_name}_deleted")
        return JSONResponse(status_code=200, content={"message": message})

    return router