from fastapi import FastAPI

from api.service_api.service_api import service_router
from api.users.users_api import user_router
app = FastAPI(docs_url="/")

from database import Base, engine
Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(service_router)