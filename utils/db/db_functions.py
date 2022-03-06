from utils.db.db import fetch, execute


async def db_check_username(user):
    # select * from User -> postgres
    query = """select * from "User" where username = :elma """
    values = {"elma": user.username}
    result = await fetch(query, False, values)
    return result


async def db_check_jwt_token(username):
    query = """select * from "User" where username= :username"""
    values = {"username": username}
    result = await fetch(query, True, values)
    if result is None:
        return False
    else:
        return True
