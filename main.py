from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
from jose import jwt
from typing import Optional
from datetime import datetime, timedelta

from database import get_db
from database.users import User
from config import algorithm, secret_key, access_token_exp_minutes

app = FastAPI(docs_url="/")

from api.service_api.service_api import service_router
from api.users.users_api import user_router
app.include_router(user_router)
app.include_router(service_router)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str


from pydantic import BaseModel


class UserOut(BaseModel):
    username: str
    email: str
    phone_number: str

    class Config:
        from_attributes = True


def verify_password(password, hashed_password):
    return password == hashed_password

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_access_token(data: dict, expire_date: Optional[timedelta] = None):
    to_encode = data.copy()
    if expire_date:
        expire = datetime.utcnow() + expire_date
    else:
        expire = datetime.utcnow() + timedelta(minutes=access_token_exp_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt

# Аутентификация пользователя
def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if user and verify_password(password, user.password):
        return user
    return None

oauth_schema = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth_schema), db: Session = Depends(get_db)):
    exception = HTTPException(status_code=404, detail="User not found")
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        username = payload.get("sub")
        if username is None:
            raise exception
    except jwt.JWTError:
        raise exception
    user = get_user(db, username)
    if user is None:
        raise exception
    return user

@app.post("/token", response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form.username, form.password)
    if not user:
        raise HTTPException(status_code=404, detail="Incorrect username or password")
    access_token_expire = timedelta(minutes=access_token_exp_minutes)
    access_token = create_access_token(data={"sub": user.username}, expire_date=access_token_expire)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/user/me", response_model=UserOut)
async def user_me(user: UserOut = Depends(get_current_user)):
    return user





