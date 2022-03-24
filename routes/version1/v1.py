import re
from fastapi import APIRouter, Depends, HTTPException, Body
import jwt
from starlette.status import HTTP_404_NOT_FOUND
from routes.version1.sera import app_sera
from utils.const import JWT_ALGORITHM, JWT_SECRET_KEY
from utils.security import oauth_scheme, login_user
from utils.db.db_functions import db_find_owner
import utils.redis_obj as re

app_v1 = APIRouter()
app_v1.include_router(app_sera, prefix="/sera")


# greet the user (fetch from owner table)
@app_v1.get("/hello/")
async def greet_user(token: str = Depends(oauth_scheme)):
    jwt_payload = jwt.decode(token, JWT_SECRET_KEY, JWT_ALGORITHM)
    user_id = jwt_payload.get("user_id")
    owner = await db_find_owner(user_id)
    if owner is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    return {f"Welcome {owner.name}!"}


# check username and password
@app_v1.post("/login")
async def get_user_validation(username: str = Body(...), password: str = Body(...)):
    # to save data in redis a key should be determined
    redis_key = f"{username}, {password}"
    result = await re.redis.get(redis_key)  # returns none or data (t/f)
    if result is not None:
        if result == b'True':
            return {"Is valid: ": True}
        else:
            return {"Is valid: ": False}

    # redis does not have the data. search it in db
    else:
        result = await login_user(username, password)  # returns true or false
        await re.redis.set(redis_key, str(result), ex=10)  # bool cannot stored in redis
        return {"Is valid (db): ": result}
