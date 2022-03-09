from datetime import datetime, timedelta
import time
import jwt
from fastapi import Depends, HTTPException
from passlib.context import CryptContext  # passwords should be hashed
from fastapi.security import OAuth2PasswordBearer
from starlette.status import HTTP_401_UNAUTHORIZED

from models.jwtuser import JWTUser
from utils.const import *
from utils.db.db_functions import db_check_username, db_check_jwt_token

pwd_context = CryptContext(schemes=["bcrypt"])
oauth_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def get_hashed_password(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        return False


# Authenticate username and password to give JWT token
async def authenticate_user(user: JWTUser):
    potential_users = await db_check_username(user.username)
    is_valid = False
    for p_user in potential_users:
        if verify_password(user.password, p_user["password"]):
            is_valid = True
            user.role = "admin"
            user.user_id = p_user["user_id"]  # get user_id from db -> jwt_user
    if is_valid:
        return user
    return None


# Create access JWT token
def create_jwt_token(user: JWTUser):
    expiration = datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_TIME_MINUTES)
    jwt_payload = {"sub": user.username, "role": user.role,
                   "user_id": user.user_id, "exp": expiration}
    jwt_token = jwt.encode(jwt_payload, JWT_SECRET_KEY, JWT_ALGORITHM)

    return jwt_token


# Check JWT token is valid or not
async def check_jwt_token(token: str = Depends(oauth_scheme)):
    try:
        jwt_payload = jwt.decode(token, JWT_SECRET_KEY, JWT_ALGORITHM)
        user_id = jwt_payload.get("user_id")
        role = jwt_payload.get("role")
        expiration = jwt_payload.get("exp")
        if time.time() < expiration:
            is_valid = await db_check_jwt_token(user_id)
            if is_valid:
                return final_checks(role)   # must be admin
    except Exception as e:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)


# Last checking and returning the final result
def final_checks(role: str):
    if role == "admin":
        return True
    else:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
