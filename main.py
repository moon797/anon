from fastapi import FastAPI
from database import  engine, Base
Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url="/")

from api.service_api.service_api import service_router
from api.users.users_api import user_router
app.include_router(user_router)
app.include_router(service_router)


