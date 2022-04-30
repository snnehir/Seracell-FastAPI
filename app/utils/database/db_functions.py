from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED
from app.models.sera import Sera
from app.utils.database.db import fetch, execute
from app.models.owner import Owner


async def db_check_username(username):
    query = """select * from users where username = :username """
    values = {"username": username}
    result = await fetch(query, False, values)
    return result


# get user by user_id (primary key)
async def db_check_jwt_token(user_id):
    query = """select * from users where user_id = :user_id"""
    values = {"user_id": user_id}
    result = await fetch(query, True, values)
    if result is None:
        return False
    else:
        return True


async def db_find_owner(user_id):
    query = """ select * from owner where owner_id = :owner_id """
    values = {"owner_id": user_id}
    result = await fetch(query, True, values)
    if result is None:
        owner = None
    else:
        owner = Owner(**result)
    return owner


async def db_get_all_sera():
    query = """ select * from sera """
    result = await fetch(query, False)
    sera_all = []
    for sera in result:
        sera_all.append(Sera(**sera))
    return sera_all


# get only my sera
async def db_get_my_sera(current_user_id):
    query = """ select * from sera
                where :current_user = any (owners)"""
    values = {"current_user": current_user_id}
    result = await fetch(query, False, values)
    sera_all = []
    for sera in result:
        sera_all.append(Sera(**sera))
    return sera_all


async def db_get_sera_by_id(sera_id):
    query = """ select * from sera
                where sera_id = :sera_id"""
    values = {"sera_id": sera_id}
    result = await fetch(query, True, values)
    return result


# insert a new sera
async def db_insert_sera(current_user_id, sera):
    array = [current_user_id]
    query = """ insert into sera(sera_name, city, zipcode, owners) 
                    values( :sera_name, :city, :zipcode, :current_user_id)
                """
    values = {
        "sera_name": sera.sera_name,
        "city": sera.city,
        "zipcode": sera.zipcode,
        "current_user_id": array,
    }
    await execute(query, False, values)


# update sera owners
async def db_add_owner_to_sera(current_user_id, sera_id):
    find_sera = await db_get_sera_by_id(sera_id)
    if find_sera is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Sera is not found!")
    else:
        result = await db_get_sera_by_id(sera_id)
        owners = result["owners"]
        if current_user_id in owners:
            return "You already own it!"
        else:
            query = """ update sera
                        set owners = array_append(owners, :current_user)
                        where sera_id = :sera_id
                        """
            values = {"sera_id": sera_id, "current_user": current_user_id}
            await execute(query, False, values)
            return "You are added to owners!"


# update sera info (update may be confusing for other owners?)
async def db_update_sera(sera_id, new_sera, user_id):
    result = await db_get_sera_by_id(sera_id)
    if result is not None:
        owners = result["owners"]
        if user_id not in owners:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail="You are not the owner!"
            )
        else:
            query = """ update sera 
                        set sera_name = :sera_name,
                            city = :city,
                            zipcode = :zipcode
                        where sera_id = :sera_id
                    """
            values = {
                "sera_id": sera_id,
                "sera_name": new_sera.sera_name,
                "city": new_sera.city,
                "zipcode": new_sera.zipcode,
            }
            await execute(query, False, values)
            return "Sera is updated!"
    # if there is no such sera
    else:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Sera is not found!")


# delete sera
async def db_delete_sera(sera_id, current_user_id):
    # find all owners of this sera
    result = await db_get_sera_by_id(sera_id)
    if result is not None:
        owners = result["owners"]
        # remove current user from owner list
        try:
            owners.remove(current_user_id)
            # if the last owner deletes, delete sera from table
            if len(owners) == 0:
                query = """ delete from sera 
                            where sera_id = :sera_id """
                values = {"sera_id": sera_id}
                result = "Sera is deleted completely!"
            # if there are other owners, just remove current user from list
            else:
                query = """ update sera 
                            set owners = :owners
                            where sera_id = :sera_id """
                values = {"sera_id": sera_id, "owners": owners}
                result = "Sera is deleted!"

            await execute(query, False, values)
            return result
        # if user is not found in owners
        except Exception:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail="You are not the owner!"
            )
    # if there is no such sera
    else:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Sera is not found!")
