from models import owner
from models.sera import Sera
from utils.db.db import fetch, execute
from models.owner import Owner


async def db_check_username(user):
    # select * from User -> postgres
    query = """select * from users where username = :username """
    values = {"username": user.username}
    result = await fetch(query, False, values)
    return result


async def db_check_jwt_token(username):
    query = """select * from users where username = :username"""
    values = {"username": username}
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


# TODO: get only my sera
async def db_get_my_sera(current_user_id):
    query = """ select * from sera
                where :current_user = any (owners)"""
    values = {"current_user": current_user_id}
    result = await fetch(query, False, values)
    sera_all = []
    for sera in result:
        sera_all.append(Sera(**sera))
    return sera_all


# TODO: get only my sera
async def db_get_sera_by_id(sera_id):
    query = """ select * from sera
                where sera_id = :sera_id"""
    values = {"sera_id": sera_id}
    result = await fetch(query, True, values)
    return result


# TODO: insert a new sera
async def db_insert_sera(current_user_id, sera):
    array = []
    array.append(current_user_id)
    query = """ insert into sera(sera_name, city, zipcode, owners) 
                    values( :sera_name, :city, :zipcode, :current_user_id)
                """
    values = {"sera_name": sera.sera_name, "city": sera.city,
              "zipcode": sera.zipcode, "current_user_id": array}
    await execute(query, False, values)


# TODO: update sera owners
async def db_add_owner_to_sera(current_user_id, sera_id):
    find_sera = await db_get_sera_by_id(sera_id)
    if find_sera is None:
        return "Sera is not found! (404)"  # burada 404 diye yazıyla dönüyorsun ama bu bir anlam ifade etmiyor. Adama HTTP 404 dönmen gerekiyor requestine karşılık. şuan HTTP 200 dönüyor içinde 404 yazıyor bu olmaz.
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


# TODO: update sera info.

# TODO: delete sera
async def db_delete_sera(sera_id, current_user_id):
    # find all owners of this sera
    result = await db_get_sera_by_id(sera_id)
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
    except Exception as e:
        return "You do not own this sera!"
