import uuid
from backend.app.database import get_db, init_db
from backend.app.core.security import hash_password
from backend.app.models.enums import UserRole
from backend.app.config import settings

def seed_database(db_path: str = None):
    init_db(db_path)
    with get_db(db_path) as conn:
        cursor = conn.cursor()
        
        # 1. Seed 12 Regional Policies
        for region_id, data in settings.INITIAL_REGIONS.items():
            cursor.execute("""
                INSERT OR IGNORE INTO regional_policies (
                    region_id, region_name, policy_version, tax_rate, shipping_fee, refund_approval_threshold, is_active
                ) VALUES (?, ?, 1, ?, ?, ?, 1)
            """, (region_id, data["name"], data["tax_rate"], data["shipping_fee"], data["refund_threshold"]))

        # 2. Seed Synthetic Accounts for All 6 Roles
        demo_users = [
            ("customer1", "customer1@fulfiliq.com", "customer123", UserRole.CUSTOMER.value, "US-EAST"),
            ("customer2", "customer2@fulfiliq.com", "customer123", UserRole.CUSTOMER.value, "US-EAST"),
            ("picker1", "picker1@fulfiliq.com", "picker123", UserRole.PICKER.value, "US-EAST"),
            ("support1", "support1@fulfiliq.com", "support123", UserRole.SUPPORT_AGENT.value, "US-EAST"),
            ("finance1", "finance1@fulfiliq.com", "finance123", UserRole.FINANCE_REVIEWER.value, "US-EAST"),
            ("manager1", "manager1@fulfiliq.com", "manager123", UserRole.STORE_MANAGER.value, "US-EAST"),
            ("admin1", "admin1@fulfiliq.com", "admin123", UserRole.ADMINISTRATOR.value, "US-EAST"),
        ]
        
        for username, email, pwd, role, region in demo_users:
            user_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, username))
            cursor.execute("""
                INSERT OR IGNORE INTO users (user_id, username, email, password_hash, role, region_id, is_active)
                VALUES (?, ?, ?, ?, ?, ?, 1)
            """, (user_id, username, email, hash_password(pwd), role, region))

        # 3. Seed Synthetic Products
        demo_products = [
            ("SKU-LAPTOP-001", "Enterprise High-Performance Laptop", "16-inch Core i9 32GB RAM", 1299.99, "Electronics"),
            ("SKU-PHONE-002", "OmniConnect 5G Smartphone", "6.7-inch OLED Display 256GB", 799.50, "Electronics"),
            ("SKU-HEADSET-003", "Noise-Cancelling Wireless Headphones", "Over-ear 40h battery life", 149.00, "Audio"),
            ("SKU-WATCH-004", "ActiveTrack Fitness Smartwatch", "Heart rate monitor & GPS", 199.99, "Wearables"),
            ("SKU-DESK-005", "Ergonomic Motorized Standing Desk", "Dual motor solid bamboo surface", 450.00, "Furniture"),
            ("SKU-CHAIR-006", "Lumbar Support Executive Office Chair", "Breathable mesh with 4D armrests", 280.00, "Furniture"),
            ("SKU-LIMITED-999", "Exclusive Collector Edition Keyboard", "Ultra-rare mechanical keyboard (Final Unit)", 350.00, "Peripherals"),
        ]
        
        for sku, name, desc, price, cat in demo_products:
            cursor.execute("""
                INSERT OR IGNORE INTO products (sku, name, description, base_price, category, is_active)
                VALUES (?, ?, ?, ?, ?, 1)
            """, (sku, name, desc, price, cat))
            
            # Seed stock across 12 regions
            for region_id in settings.INITIAL_REGIONS.keys():
                # For SKU-LIMITED-999, set exactly 1 unit on hand in US-EAST to test race condition!
                if sku == "SKU-LIMITED-999" and region_id == "US-EAST":
                    stock_qty = 1
                elif sku == "SKU-LIMITED-999":
                    stock_qty = 0
                else:
                    stock_qty = 50
                    
                cursor.execute("""
                    INSERT OR IGNORE INTO stock_items (sku, region_id, on_hand, reserved, version)
                    VALUES (?, ?, ?, 0, 1)
                """, (sku, region_id, stock_qty))
                
    print("Database successfully initialized and seeded with synthetic data!")

if __name__ == "__main__":
    seed_database()
