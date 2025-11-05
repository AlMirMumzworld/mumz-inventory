from fastapi import APIRouter

from src.apis.crud import router as crud_router
from src.apis.stock import router as stock_router


routes = APIRouter()

routes.include_router(stock_router, tags=["Stock"])
routes.include_router(crud_router, prefix="/crud", tags=["CRUD Operations"])
