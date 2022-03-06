from pydantic import BaseModel


class Sera(BaseModel):
    SeraName: str
    City: str
    Zipcode: str
