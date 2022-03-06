from fastapi import Query
from pydantic import BaseModel


class Owner(BaseModel):
    name: str
    surname: str
    phone_number: str
    mail: str = Query(..., regex="^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$")

