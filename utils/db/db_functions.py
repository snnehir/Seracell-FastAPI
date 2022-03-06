from models.sera import Sera
from utils.db.db import fetch, execute
from models.owner import Owner


async def db_check_username(user):
    # select * from User -> postgres
    query = """select * from "User" where username = :username """
    values = {"username": user.username}
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


async def db_find_owner(user_id):
    query = """ select * from "Owner" where "OwnerID"= :owner_id """
    values = {"owner_id": user_id}
    result = await fetch(query, True, values)
    if result is None:
        owner = None
    else:
        owner = Owner(**result)
    return owner


async def db_get_all_sera():
    query = """ select * from "Sera" """
    result = await fetch(query, False)
    sera_all = []
    for sera in result:
        sera_all.append(Sera(**sera))
    return sera_all


# TODO: get only my sera
async def db_get_my_sera(current_user_id):
    query = """ select * from "HasSera" inner join "Sera" 
                on "Sera"."SeraID" = "HasSera"."SeraID"
                where "HasSera"."OwnerID" = :current_user """
    values = {"current_user": current_user_id}
    result = await fetch(query, False, values)
    sera_all = []
    for sera in result:
        sera_all.append(Sera(**sera))
    return sera_all


# TODO: insert sera
async def db_insert_sera(current_user_id, sera):
    add_query = """ insert into "Sera"("SeraName","City","Zipcode") 
                values (:sera_name, :city, :zipcode) returning "SeraID" """
    add_values = {"sera_name": sera.SeraName, "city": sera.City, "zipcode": sera.Zipcode}
    created_sera_id = await execute(add_query, False, add_values)

    # add to relation table
    relation_query = """ insert into "HasSera"("SeraID","OwnerID") values (:created_sera_id, :current_user_id) """
    relation_values = {"created_sera_id": created_sera_id, "current_user_id": current_user_id}
    await execute(relation_query, False, relation_values)


# TODO: update sera

# TODO: delete sera
async def db_delete_sera(sera_id, current_user_id):
    relation_query = """ delete from "HasSera"  WHERE "SeraID" = :sera_id and "OwnerID" = :current_user_id """
    relation_values = {"sera_id": sera_id, "current_user_id": current_user_id}
    await execute(relation_query, False, relation_values)

    query = """ delete from "Sera"  WHERE "SeraID" = :sera_id """
    values = {"sera_id": sera_id}
    await execute(query, False, values)