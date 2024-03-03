from fastapi import FastAPI
from app.api.endpoints.endpoints import upload_hired_employees, root, router
from app.api.database.base_class import Base
from app.api.database.database_connection import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)

