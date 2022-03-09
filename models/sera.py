from pydantic import BaseModel


class Sera(BaseModel):
    sera_name: str
    city: str
    zipcode: str
