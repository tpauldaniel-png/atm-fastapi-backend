from pydantic import BaseModel
from datetime import date, datetime
from uuid import UUID


class UserCreate(BaseModel):
    first_name : str
    last_name : str
    date_of_birth : date
    phone_no : str
    corresponding_address : str
    email : str
    password : str

class Userout(BaseModel):
    user_id : UUID
    first_name : str
    last_name : str
    date_of_birth : date
    phone_no : str
    corresponding_address : str
    email : str

    class Config:
        from_attributes = True


class UserCreateResponse(BaseModel):
    message : str
    user : Userout

class UsersResponse(BaseModel):
    users : list[Userout]
    





