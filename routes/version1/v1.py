from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED

from models.sera import Sera
from utils.db.db_functions import db_find_owner, db_get_all_sera, db_get_my_sera, db_insert_sera, db_delete_sera

app_v1 = APIRouter()


# greet the user (fetch from owner table)
@app_v1.get("/hello/{user_id}")
#burada iki opsiyonumuz var. Ya user_id'yi senin yaptığın gibi url içinde alacağız.
# İkinci seçenek ise query parameter olarak alacağız. duruma göre ikisi de kullanılabilir.
# url'den {user_id} silersen ve fonksiyon içinde yine de user_id ' yi alırsan query param'a çevirmiş olursun.
async def hello_world(user_id: int):
    owner = await db_find_owner(user_id)
    if owner is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    return {f"Welcome {owner.Name}!"}


# TODO: router for "sera" operations
# Returns all sera from db
@app_v1.get("/sera/all")
async def get_my_greenhouses():
    sera_all = await db_get_all_sera()
    if sera_all is None:
        return {"There is no greenhouse!"}
    return {"All greenhouses: " + str(sera_all)}


@app_v1.get("/sera/my/{current_user_id}")
# burada endpointi isimlendirirken, my yazmak pek olmamış. Genelde şahsi şeyler içeren isimlendirmeler yazılmaz.
# admin olabilir ama my, me, you, other gibi şeyler kullanımı tavsiye edilmez. daha uygun olan isimlendirme
# /sera/{current_user_id} olur yani direk olayı belli zaten, o user'a ait seraları dönecek
async def get_all_greenhouses(current_user_id: int):
    sera_all = await db_get_my_sera(current_user_id)
    if sera_all is None:
        return {"You do not have any greenhouse!"}
    else:
        output = ""
        # aşağıdaki satır için bir kısa yol var genelde o kullanılır. Senin de aklında olsun. Eğer bir list'im varsa
        # ve o listi string'e çevirecek araya - veya virgül gibi şeyler koyacaksam join kullanılır. Örneğin
        # a = ["s1","s2","s3"]
        # ' - '.join(a)
        for sera in sera_all:
            output += str(sera) + ' - '  # \n does not work
        return {f"My greenhouses: {output} "}


@app_v1.post("/sera/new/{current_user_id}", status_code=HTTP_201_CREATED)
# burada yine isimlendirme yaparken new kullanmak doğru değil. POST zaten bişeyin create edileceği anlamına geliyor
# dolayısı ile /sera demek zaten POST olması itibariyle sera POST yani create edilecek anlamı taşır. Bu yeterlidir.
# sonrasında current_user_id yi ise query parameter olarak al ki kafa karıştırmasın endpointte.
async def get_my_greenhouses(current_user_id: int, sera: Sera):
    await db_insert_sera(current_user_id, sera)
    return {"result": "sera is created"}


@app_v1.delete("/sera/delete/{sera_id}")
# DELETE zaten http methodunun adı, endpoint url'ine delete yazmak olmaz. bu da sade /sera olmalı yani DELETE /sera
# oldukça anlamlı. sera_id query param olarak al.
async def delete_greenhouse(current_user_id: int, sera_id: int):
    await db_delete_sera(sera_id, current_user_id)
    return {"result": "sera is deleted"}