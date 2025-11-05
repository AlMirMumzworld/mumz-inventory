-- Countries Table
CREATE TABLE countries (
    id SERIAL PRIMARY KEY,
    code VARCHAR(3) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL
);

-- Vendors Table
CREATE TABLE vendors (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true
);

-- Business Models (Fulfillment Types)
CREATE TABLE business_models (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL
);

-- Priority Matrix: Business Model Priorities per Country
CREATE TABLE business_model_priorities (
    id SERIAL PRIMARY KEY,
    country_id INTEGER NOT NULL REFERENCES countries(id),
    business_model_id INTEGER NOT NULL REFERENCES business_models(id),
    priority INTEGER NOT NULL,
    UNIQUE(country_id, business_model_id)
);

-- Priority Matrix: Vendor Priorities per Country and Business Model
CREATE TABLE vendor_priorities (
    id SERIAL PRIMARY KEY,
    country_id INTEGER NOT NULL REFERENCES countries(id),
    business_model_id INTEGER NOT NULL REFERENCES business_models(id),
    vendor_id INTEGER NOT NULL REFERENCES vendors(id),
    priority INTEGER NOT NULL,
    UNIQUE(country_id, business_model_id, vendor_id)
);

-- Inventory Table
CREATE TABLE inventory (
    id SERIAL PRIMARY KEY,
    sku VARCHAR(100) NOT NULL,
    country_id INTEGER NOT NULL REFERENCES countries(id),
    vendor_id INTEGER NOT NULL REFERENCES vendors(id),
    business_model_id INTEGER NOT NULL REFERENCES business_models(id),
    stock INTEGER NOT NULL DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(sku, country_id, vendor_id, business_model_id)
);

-- Indexes
CREATE INDEX idx_inventory_sku_country ON inventory(sku, country_id);
CREATE INDEX idx_inventory_stock ON inventory(stock) WHERE stock > 0;

-- ============================================
-- SAMPLE DATA
-- ============================================

INSERT INTO countries (code, name) VALUES 
    ('UAE', 'United Arab Emirates'),
    ('KSA', 'Kingdom of Saudi Arabia');

INSERT INTO business_models (code, name) VALUES 
    ('RETAIL', 'Retail'),
    ('FBM', 'Fulfillment by Merchant'),
    ('FBS', 'Fulfillment by Store'),
    ('DS', 'Drop Shipping');

INSERT INTO vendors (code, name) VALUES 
    ('MZ', 'Mumzworld'),
    ('PHCTY', 'Pharmaciaty'),
    ('CRF', 'Carrefour'),
    ('ANDR', 'Andador');

-- Business Model Priorities for UAE
INSERT INTO business_model_priorities (country_id, business_model_id, priority) VALUES 
    ((SELECT id FROM countries WHERE code = 'UAE'), (SELECT id FROM business_models WHERE code = 'RETAIL'), 1),
    ((SELECT id FROM countries WHERE code = 'KSA'), (SELECT id FROM business_models WHERE code = 'RETAIL'), 1),
    ((SELECT id FROM countries WHERE code = 'UAE'), (SELECT id FROM business_models WHERE code = 'FBS'), 2),
    ((SELECT id FROM countries WHERE code = 'UAE'), (SELECT id FROM business_models WHERE code = 'FBM'), 3),
    ((SELECT id FROM countries WHERE code = 'UAE'), (SELECT id FROM business_models WHERE code = 'DS'), 4);

-- Vendor Priorities for UAE + RETAIL
INSERT INTO vendor_priorities (country_id, business_model_id, vendor_id, priority) VALUES 
    ((SELECT id FROM countries WHERE code = 'UAE'), (SELECT id FROM business_models WHERE code = 'RETAIL'), (SELECT id FROM vendors WHERE code = 'MZ'), 1),
    ((SELECT id FROM countries WHERE code = 'KSA'), (SELECT id FROM business_models WHERE code = 'RETAIL'), (SELECT id FROM vendors WHERE code = 'MZ'), 2),
    ((SELECT id FROM countries WHERE code = 'UAE'), (SELECT id FROM business_models WHERE code = 'FBS'), (SELECT id FROM vendors WHERE code = 'CRF'), 3);

-- Sample Inventory for SKU-12345 in UAE
INSERT INTO inventory (sku, country_id, vendor_id, business_model_id, stock) VALUES 
    ('SKU-12345', (SELECT id FROM countries WHERE code = 'UAE'), (SELECT id FROM vendors WHERE code = 'MZ'), (SELECT id FROM business_models WHERE code = 'RETAIL'), 10),
    ('SKU-12345', (SELECT id FROM countries WHERE code = 'KSA'), (SELECT id FROM vendors WHERE code = 'MZ'), (SELECT id FROM business_models WHERE code = 'RETAIL'), 40),
    ('SKU-12345', (SELECT id FROM countries WHERE code = 'UAE'), (SELECT id FROM vendors WHERE code = 'CRF'), (SELECT id FROM business_models WHERE code = 'FBS'), 80),
    ('SKU-12345', (SELECT id FROM countries WHERE code = 'UAE'), (SELECT id FROM vendors WHERE code = 'PHCTY'), (SELECT id FROM business_models WHERE code = 'FBM'), 150);

-- ============================================
-- QUERY TO GET INVENTORY WITH PRIORITY
-- ============================================

-- Get inventory for a SKU in a country, ordered by priority
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
    i.sku = 'SKU-12345'
    AND c.code = 'UAE'
    AND i.stock > 0
    AND v.is_active = true
ORDER BY 
    bmp.priority ASC,
    vp.priority ASC,
    i.stock DESC;

-- Get only the top priority vendor (what your API returns)
SELECT 
    i.sku,
    c.code AS country_code,
    v.code AS vendor_code,
    v.name AS vendor_name,
    bm.code AS business_model_code,
    i.stock
FROM inventory i
INNER JOIN countries c ON i.country_id = c.id
INNER JOIN vendors v ON i.vendor_id = v.id
INNER JOIN business_models bm ON i.business_model_id = bm.id
INNER JOIN business_model_priorities bmp ON bmp.country_id = c.id AND bmp.business_model_id = bm.id
INNER JOIN vendor_priorities vp ON vp.country_id = c.id AND vp.business_model_id = bm.id AND vp.vendor_id = v.id
WHERE 
    i.sku = 'SKU-12345'
    AND c.code = 'UAE'
    AND i.stock > 0
    AND v.is_active = true
ORDER BY 
    bmp.priority ASC,
    vp.priority ASC,
    i.stock DESC
LIMIT 1;