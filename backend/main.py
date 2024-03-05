from fastapi import FastAPI
from app.api.endpoints.post_requests import router as post_router
from app.api.endpoints.get_requests import router as get_router
from app.api.database.base_class import Base
from app.api.database.database_connection import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post_router)
app.include_router(get_router)