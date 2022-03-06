from utils.db.db_object import db


async def execute(query, is_many, values=None):
    if is_many:
        await db.execute_many(query=query, values=values)
    else:
        return await db.execute(query=query, values=values)  # id of inserted sera will be returned


async def fetch(query, is_one, values=None):
    if is_one:
        result = await db.fetch_one(query=query, values=values)
        if result is None:
            out = None
        else:
            out = dict(result)
    else:
        out = []
        result = await db.fetch_all(query=query, values=values)
        for row in result:
            out.append(dict(row))
    return out
