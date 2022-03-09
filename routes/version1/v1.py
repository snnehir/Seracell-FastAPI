import re
from fastapi import APIRouter, Depends, HTTPException
import jwt
from starlette.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED
from utils.const import JWT_ALGORITHM, JWT_SECRET_KEY
from utils.security import oauth_scheme
from models.sera import Sera
from utils.db.db_functions import db_add_owner_to_sera, db_find_owner, db_get_all_sera, db_get_my_sera, db_insert_sera, db_delete_sera

app_v1 = APIRouter()


# greet the user (fetch from owner table)
# user_id -> query parameter
@app_v1.get("/hello/")
async def greet_user(user_id: int):
    owner = await db_find_owner(user_id)
    if owner is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    return {f"Welcome {owner.name}!"}


# TODO: router for "sera" operations
# Returns all sera from db
@app_v1.get("/sera/all")
async def get_my_greenhouses():
    sera_all = await db_get_all_sera()
    if sera_all is None:
        return {"There is no greenhouse!"}
    return {f"All greenhouses {len(sera_all)}: {str(sera_all)}"}


# Return all sera of current user
# burda işte artık adamın user_id'si jwt token'a gömmen lazım. şu anda sadece username'i gömmüşsün. id yi gömmek daha mantıklı. gömünde burada jwt tokeni decode edeceksin içinde user_id'yi alacaksın ve dolayııs ile artık {current_user_id} parametresine ihtiyacın kalmayacak.
# user_id gereken her endpoint'te jwt token'ı decode etmem doğru mu?
@app_v1.get("/sera/")
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


# current_user_id -> jwt token
@app_v1.post("/sera/", status_code=HTTP_201_CREATED)
async def create_greenhouse(sera: Sera, token: str = Depends(oauth_scheme)):
    jwt_payload = jwt.decode(token, JWT_SECRET_KEY, JWT_ALGORITHM)
    user_id = jwt_payload.get("user_id")
    # print(">>> user: " + str(user_id))
    await db_insert_sera(user_id, sera)
    return {"result": "New greenhouse is created"}


# Add another owner to existing sera
# sera/owner mantıklı.
@ app_v1.post("/sera/owner/", status_code=HTTP_201_CREATED)
async def add_another_owner_to_sera(sera_id: int, token: str = Depends(oauth_scheme)):
    jwt_payload = jwt.decode(token, JWT_SECRET_KEY, JWT_ALGORITHM)
    user_id = jwt_payload.get("user_id")
    result = await db_add_owner_to_sera(user_id, sera_id)
    return {"result": result}


# sera_id -> query parameter
@ app_v1.delete("/sera/")
# tüm endpointlerinde aynı current_user_id jwt token içinden almalısın ve sadece o adama ait veritabanı kayıtlarında işlem yapabilmelisin.
async def delete_greenhouse(sera_id: int, token: str = Depends(oauth_scheme)):
    jwt_payload = jwt.decode(token, JWT_SECRET_KEY, JWT_ALGORITHM)
    user_id = jwt_payload.get("user_id")
    result = await db_delete_sera(sera_id, user_id)
    return {"result": result}
