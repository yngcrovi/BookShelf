from pydantic import BaseModel
from datetime import date

class GetIdBookDTO(BaseModel):
    id: int
    name: str
    author: str
    date_of_publication: date

class GetUserSaltDTO(BaseModel):
    salt: bytes

class GetUserDTO(BaseModel):
    id: int
    username: str
    hash_password: bytes