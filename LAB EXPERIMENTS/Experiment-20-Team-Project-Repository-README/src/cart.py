"""
Module: Shopping Cart & Checkout
Author: Student 3 (Collaborator)
Feature Branch: feature-cart
Course: CSA10 - Software Engineering
"""

def calculate_total(cart_items, tax_rate=0.18):
    """Calculate cart subtotal, taxes, and grand total."""
    subtotal = sum(item["price"] * item.get("quantity", 1) for item in cart_items)
    tax = subtotal * tax_rate
    grand_total = subtotal + tax
    return {
        "subtotal": subtotal,
        "tax": tax,
        "grand_total": grand_total
    }

if __name__ == "__main__":
    test_cart = [
        {"id": 101, "item": "Laptop (16GB RAM)", "price": 55000, "quantity": 1},
        {"id": 102, "item": "Noise-Cancelling Headphones", "price": 4500, "quantity": 2}
    ]
    summary = calculate_total(test_cart)
    print("Testing Cart Module Summary:")
    print(f"Subtotal: Rs. {summary['subtotal']}")
    print(f"Tax (18%): Rs. {summary['tax']}")
    print(f"Grand Total: Rs. {summary['grand_total']}")
