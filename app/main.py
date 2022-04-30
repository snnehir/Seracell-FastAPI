import pickle

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_401_UNAUTHORIZED
from app.utils.const import REDIS_URL, TESTING, TOKEN_INVALID_MATCH_MESSAGE
from app.utils.database.db_object import db
from app.models.jwtuser import JWTUser
from app.routes.version1.v1 import app_v1
from app.utils.security import authenticate_user, create_jwt_token, check_jwt_token
import app.utils.redis_obj as re
from app.utils.redis_obj import check_test_redis
import aioredis

app = FastAPI(title="Seracell Demo")
# Authentication dependency (check jwt token) & test dependency
app.include_router(
    app_v1,
    prefix="/v1",
    dependencies=[Depends(check_jwt_token), Depends(check_test_redis)],
)


# connect
@app.on_event("startup")
async def connect_db():
    if not TESTING:
        await db.connect()
        re.redis = await aioredis.from_url(REDIS_URL)


# disconnect
@app.on_event("shutdown")
async def disconnect_db():
    if not TESTING:
        await db.disconnect()
        await re.redis.close()


@app.get("/")
async def hello_world():
    return {"Hello FastAPI!"}


# create jwt token
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # use cache to increase the rps (request per seconds)
    if not TESTING:
        redis_key = f"token:{form_data.username}, {form_data.password}"
        user_redis = await re.redis.get(redis_key)  # look cache
        # if the user is not in cache
        if not user_redis:
            # create user
            jwt_user_dict = {
                "username": form_data.username,
                "password": form_data.password,
            }
            jwt_user = JWTUser(**jwt_user_dict)
            # authenticate
            user = await authenticate_user(jwt_user)
            # check if there is such user
            if user is None:
                # HTTP exception must be raised
                raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail=TOKEN_INVALID_MATCH_MESSAGE)
            # add it to cache if there is such user
            else:
                await re.redis.set(redis_key, pickle.dumps(user))
        # data is in cache
        else:
            user = pickle.loads(user_redis)
    # if redis is none (for test container)
    else:
        jwt_user_dict = {"username": form_data.username, "password": form_data.password}
        jwt_user = JWTUser(**jwt_user_dict)
        user = await authenticate_user(jwt_user)
        # check if there is such user
        if user is None:
            # HTTP exception must be raised
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
    # create jwt token if there is such user in db or cache
    jwt_token = create_jwt_token(user)
    return {"access_token": jwt_token}  # access_token -> swagger standard
