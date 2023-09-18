import typing as t
from pydantic import BaseModel, Field


class Pet(BaseModel):
    name: str = Field(...)
    animal_type: str = Field(...)
    age: int = Field(...)
    photo: str = Field(None)

class PetsCollection(BaseModel):
    pets: t.List[Pet] = Field(...)

class Api(BaseModel):
    key: str = Field(...)