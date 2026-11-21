"""
Module: Product Catalog
Author: Student 2 (Collaborator)
Feature Branch: feature-catalog
Course: CSA10 - Software Engineering
"""

def get_catalog():
    """Return available products and catalog pricing."""
    return [
        {"id": 101, "item": "Laptop (16GB RAM)", "category": "Electronics", "price": 55000},
        {"id": 102, "item": "Noise-Cancelling Headphones", "category": "Audio", "price": 4500},
        {"id": 103, "item": "Mechanical Keyboard", "category": "Peripherals", "price": 3200}
    ]

if __name__ == "__main__":
    print("Testing Catalog Module:")
    for product in get_catalog():
        print(f"[{product['id']}] {product['item']} - Rs. {product['price']}")
