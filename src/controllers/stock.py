from sqlalchemy import text
from sqlalchemy.orm import Session


class StockController:
    """Stock controller to handle item-specific operations"""

    def __init__(self, db: Session):
        self.db = db

    def get_inventory(self, sku: str, country: str):
        """Get stock of an item by sku and country code"""

        stmt = f"""
            SELECT 
                i.sku,
                c.code AS country_code,
                v.code AS vendor_code,
                v.name AS vendor_name,
                bm.code AS business_model_code,
                bm.name AS business_model_name,
                i.stock,
                bmp.priority AS business_model_priority,
                vp.priority AS vendor_priority
            FROM inventory i
            INNER JOIN countries c ON i.country_id = c.id
            INNER JOIN vendors v ON i.vendor_id = v.id
            INNER JOIN business_models bm ON i.business_model_id = bm.id
            INNER JOIN business_model_priorities bmp ON bmp.country_id = c.id AND bmp.business_model_id = bm.id
            INNER JOIN vendor_priorities vp ON vp.country_id = c.id AND vp.business_model_id = bm.id AND vp.vendor_id = v.id
            WHERE 
                lower(i.sku) = '{sku.lower()}'
                AND lower(c.code) = '{country.lower()}'
                AND i.stock > 0
                AND v.is_active = true
            ORDER BY 
                bmp.priority ASC,
                vp.priority ASC,
                i.stock DESC;
        """
        items = self.db.execute(text(stmt)).all()
        return [
            {
                "sku": item[0],
                "country_code": item[1],
                "vendor": item[2],
                "vendor_name": item[3],
                "business_model": item[4],
                "business_model_name": item[5],
                "stock": item[6],
                "business_model_priority": item[7],
                "vendor_priority": item[8]
            }
            for item in items]
