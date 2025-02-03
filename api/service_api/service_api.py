from database.service import *
from fastapi import APIRouter
from pydantic import BaseModel, constr
import re

service_router= APIRouter(tags=["Работа с сервисом"], prefix="/service")

def mail_checker(email):
    regex = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
    if re.match(regex, email):
        return True
    return False

def check_phone_number(phone_number):
    regex = r"^998(90|91|92|93|94|95|96|97|98|99|33)\d{7}$"
    if re.match(regex, phone_number):
        return True
    else:
        return False

def check_user_name(username):
     regex = r"^[a-zA-Z0-9._]{1,8}$"
     if re.match(regex, username):
        return True
     else:
         return False

class User(BaseModel):
    username : str
    phone_number : str
    email : str
    password: str
    country : str | None=None
    birthday : str|  None= None
@service_router.post("/registration")
async def registration(user_model :User):
    data = dict(user_model)
    mail_validator = mail_checker(user_model.email)
    number_validator = check_phone_number(user_model.phone_number)
    username_validator = check_user_name(user_model.username)
    if not username_validator:
            return {"status": 1, "message": "Введите имя пользователя в правильном формате"}
    if not number_validator:
            return {"status": 1, "message": "Такой номер телефона не поддерживается"}
    if not mail_validator:
        return {"status":1, "message":"Введите email в правильном формате"}
    result = registration_db(**data)
    if result:
        return {"status": 0, "message": "Регистрация прошла успешно!"}






