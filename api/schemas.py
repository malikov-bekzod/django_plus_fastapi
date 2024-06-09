
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class LoginModel(BaseModel):
    username: str
    password: str

class RegisterModel(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    email: str

class CategorySchema(BaseModel):
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True


class ProductSchema(BaseModel):
    name: str
    description: Optional[str]
    price: float
    categories: list

    class Config:
        orm_mode = True

class OrderSchema(BaseModel):
    user_id: int
    total_amount: float
    products: list

    class Config:
        orm_mode = True

class JwtModel(BaseModel):
    authjwt_secret_key: str = '3ab42577ea4c274120ac14a8cd6d9b307f0b17f94d39a074b5073efe9c9fdbcb'