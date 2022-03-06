from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED

from models.sera import Sera
from utils.db.db_functions import db_find_owner, db_get_all_sera, db_get_my_sera, db_insert_sera, db_delete_sera

app_v1 = APIRouter()


# greet the user (fetch from owner table)
@app_v1.get("/hello/{user_id}")
async def hello_world(user_id: int):
    owner = await db_find_owner(user_id)
    if owner is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    return {f"Welcome {owner.Name}!"}


# TODO: router for "sera" operations
# Returns all sera from db
@app_v1.get("/sera/all")
async def get_my_greenhouses():
    sera_all = await db_get_all_sera()
    if sera_all is None:
        return {"There is no greenhouse!"}
    return {"All greenhouses: " + str(sera_all)}


@app_v1.get("/sera/my/{current_user_id}")
async def get_all_greenhouses(current_user_id: int):
    sera_all = await db_get_my_sera(current_user_id)
    if sera_all is None:
        return {"You do not have any greenhouse!"}
    else:
        output = ""
        for sera in sera_all:
            output += str(sera) + ' - '  # \n does not work
        return {f"My greenhouses: {output} "}


@app_v1.post("/sera/new/{current_user_id}", status_code=HTTP_201_CREATED)
async def get_my_greenhouses(current_user_id: int, sera: Sera):
    await db_insert_sera(current_user_id, sera)
    return {"result": "sera is created"}


@app_v1.delete("/sera/delete/{sera_id}")
async def delete_greenhouse(current_user_id: int, sera_id: int):
    await db_delete_sera(sera_id, current_user_id)
    return {"result": "sera is deleted"}