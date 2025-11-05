from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.controllers.db import DatabaseController
from src.schemas.tables import TableNames

router = APIRouter()


@router.get("/{table}")
def get_items(table: TableNames, db: Session = Depends(get_db)):
    """API to get an item by id"""

    controller = DatabaseController(db)
    model = controller.get_model_class(table_name=table)
    items = controller.read_many(model=model)
    return jsonable_encoder(items)


@router.get("/{table}/{item_id}")
def get_item(table: TableNames, item_id: int, db: Session = Depends(get_db)):
    """API to get an item by id"""

    controller = DatabaseController(db)
    model = controller.get_model_class(table_name=table)
    item = controller.read(model=model, item_id=item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    return item


@router.post("/{table}")
def create_item(table: TableNames, data: dict, db: Session = Depends(get_db)):
    """API to create an item"""

    controller = DatabaseController(db)
    model = controller.get_model_class(table_name=table)
    return controller.create(model=model, data=data)


@router.put("/{table}/{item_id}")
def update_item(table: TableNames, item_id: int, data: dict, db: Session = Depends(get_db)):
    """API to update an item by id"""

    controller = DatabaseController(db)
    model = controller.get_model_class(table)
    item = controller.read(model=model, item_id=item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    return controller.update(item=item, data=data)


@router.delete("/{table}/{item_id}")
def delete_item(table: TableNames, item_id: int, db: Session = Depends(get_db)):
    """API to delete an item by id"""

    controller = DatabaseController(db)
    model = controller.get_model_class(table)
    item = controller.read(model=model, item_id=item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    return controller.delete(item=item)
