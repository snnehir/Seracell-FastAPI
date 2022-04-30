from fastapi import Query
from pydantic import BaseModel


class Sera(BaseModel):
    sera_name: str
    city: str
    zipcode: str = Query(None, max_length=5, min_length=5, regex="^([0-9]+)$")
