from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.controllers.stock import StockController


router = APIRouter()


@router.get("/stock")
def get_stock(sku: str, country: str, db: Session = Depends(get_db)):
    """API to get stock of an item by sku and country code"""

    controller = StockController(db)
    stock = controller.get_inventory(sku=sku, country=country)
    return jsonable_encoder(stock)
