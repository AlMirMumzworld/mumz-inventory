from enum import Enum

from src.models.inventory import Inventory
from src.models.country import Country
from src.models.business_model import BusinessModel
from src.models.vendor import Vendor
from src.models.business_model_priority import BusinessModelPriority
from src.models.vendor_priority import VendorPriority


class TableNames(str, Enum):
    """Enum for database table names."""

    INVENTORY = Inventory.__tablename__
    COUNTRY = Country.__tablename__
    BUSINESS_MODEL = BusinessModel.__tablename__
    VENDOR = Vendor.__tablename__
    BUSINESS_MODEL_PRIORITY = BusinessModelPriority.__tablename__
    VENDOR_PRIORITY = VendorPriority.__tablename__
