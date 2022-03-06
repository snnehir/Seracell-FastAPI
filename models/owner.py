from fastapi import Query
from pydantic import BaseModel


class Owner(BaseModel):
    Name: str
    Surname: str
    PhoneNumber: str
    Mail: str = Query(..., regex="^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$")

