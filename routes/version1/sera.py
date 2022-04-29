import jwt
from fastapi import APIRouter, Depends, Body
from starlette.status import HTTP_201_CREATED

from models.sera import Sera
from utils.const import JWT_SECRET_KEY, JWT_ALGORITHM
from utils.db.db_functions import (
    db_get_all_sera,
    db_get_my_sera,
    db_insert_sera,
    db_delete_sera,
    db_add_owner_to_sera,
    db_update_sera,
)
from utils.security import oauth_scheme

# Sera operations will be done from this router
app_sera = APIRouter()


# Return all sera in the db
@app_sera.get("/all")
async def get_my_greenhouses():
    sera_all = await db_get_all_sera()
    if sera_all is None:
        return {"There is no greenhouse!"}
    return {f"All greenhouses {len(sera_all)}: {str(sera_all)}"}


# Return all sera of current user
@app_sera.get("/")
async def get_all_greenhouses(token: str = Depends(oauth_scheme)):
    # get user_id from jwt token
    jwt_payload = jwt.decode(token, JWT_SECRET_KEY, JWT_ALGORITHM)
    user_id = jwt_payload.get("user_id")
    # select only authenticated user's sera
    sera_all = await db_get_my_sera(user_id)
    if sera_all is None:
        return {"You do not have any greenhouse!"}
    else:
        return {f"My greenhouses {len(sera_all)}:  {sera_all} "}


# Add new sera
@app_sera.post("/", status_code=HTTP_201_CREATED)
async def create_greenhouse(sera: Sera, token: str = Depends(oauth_scheme)):
    jwt_payload = jwt.decode(token, JWT_SECRET_KEY, JWT_ALGORITHM)
    user_id = jwt_payload.get("user_id")
    await db_insert_sera(user_id, sera)
    return {"result": "New greenhouse is created"}


# Add another owner to existing sera
@app_sera.post("/owner/", status_code=HTTP_201_CREATED)
async def add_another_owner_to_greenhouse(
    sera_id: int, token: str = Depends(oauth_scheme)
):
    jwt_payload = jwt.decode(token, JWT_SECRET_KEY, JWT_ALGORITHM)
    user_id = jwt_payload.get("user_id")
    result = await db_add_owner_to_sera(user_id, sera_id)
    return {"result": result}


# Update sera
@app_sera.put("/{sera_id}")
async def update_greenhouse(
    sera_id: int, new_sera: Sera = Body(...), token: str = Depends(oauth_scheme)
):
    jwt_payload = jwt.decode(token, JWT_SECRET_KEY, JWT_ALGORITHM)
    user_id = jwt_payload.get("user_id")
    result = await db_update_sera(sera_id, new_sera, user_id)
    return {"result": result}


# Delete sera
@app_sera.delete("/")
async def delete_greenhouse(sera_id: int, token: str = Depends(oauth_scheme)):
    jwt_payload = jwt.decode(token, JWT_SECRET_KEY, JWT_ALGORITHM)
    user_id = jwt_payload.get("user_id")
    result = await db_delete_sera(sera_id, user_id)
    return {"result": result}
