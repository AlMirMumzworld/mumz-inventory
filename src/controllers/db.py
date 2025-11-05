from sqlalchemy.orm import Session

from src.models.inventory import Inventory
from src.models.country import Country
from src.models.business_model import BusinessModel
from src.models.vendor import Vendor
from src.models.business_model_priority import BusinessModelPriority
from src.models.vendor_priority import VendorPriority
from src.schemas.tables import TableNames


class DatabaseController:
    """Database controller to handle CRUD operations"""

    def __init__(self, db: Session):
        self.db = db
        self.tables: dict[str, type] = {
            TableNames.INVENTORY: Inventory,
            TableNames.COUNTRY: Country,
            TableNames.BUSINESS_MODEL: BusinessModel,
            TableNames.VENDOR: Vendor,
            TableNames.BUSINESS_MODEL_PRIORITY: BusinessModelPriority,
            TableNames.VENDOR_PRIORITY: VendorPriority,
        }

    def get_model_class(self, table_name: TableNames) -> type:
        """Get SQLAlchemy model class by table name."""

        return self.tables[table_name]

    def read(self, model, item_id: int):
        """Get an item by id"""

        return self.db.query(model).filter(model.id == item_id).first()

    def read_many(self, model):
        """Get an item by id"""

        return self.db.query(model).all()

    def create(self, model, data: dict):
        """Create a new item"""

        new_item = model(**data)
        self.db.add(new_item)
        self.db.commit()
        self.db.refresh(new_item)
        return new_item

    def update(self, item, data: dict):
        """Update an existing item by id"""

        for key, value in data.items():
            setattr(item, key, value)

        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item):
        """Delete an item by id"""

        self.db.delete(item)
        self.db.commit()
        return item
