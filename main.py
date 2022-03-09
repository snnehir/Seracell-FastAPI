from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_401_UNAUTHORIZED
from utils.db.db_object import db
from models.jwtuser import JWTUser
from routes.version1.v1 import app_v1
from utils.security import authenticate_user, create_jwt_token, check_jwt_token

app = FastAPI(title="Seracell Demo")
# Authentication dependency (check jwt token)
app.include_router(app_v1, prefix="/v1",
                   dependencies=[Depends(check_jwt_token)])


# connect
@app.on_event("startup")
async def connect_db():
    await db.connect()


# disconnect
@app.on_event("shutdown")
async def disconnect_db():
    await db.disconnect()


@app.get("/")
async def hello_world():
    return {"HelloFastAPI!"}


# create jwt token
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    jwt_user_dict = {"username": form_data.username,
                     "password": form_data.password}
    jwt_user = JWTUser(**jwt_user_dict)
    user = await authenticate_user(jwt_user)
    # check if there is such user
    if user is None:
        # HTTP exception must be raised
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
    # create jwt token if there is such user in db
    jwt_token = create_jwt_token(user)
    return {"access_token": jwt_token}  # access_token -> swagger standard
