"""
Experiment 06: Online Food Delivery System - Domain Model & Simulation
Student: Angulakshmi S (Reg No: 192524402)
Course: CSA10 - Software Engineering
Course Outcome: CO1

This Python program implements the exact Object-Oriented design specified in the
UML Class Diagram for the Online Food Delivery System, verifying attributes,
methods, and relationships (Association, Aggregation, Composition).
"""

from datetime import datetime
from typing import List, Optional

class FoodItem:
    def __init__(self, item_id: int, item_name: str, price: float, category: str):
        self.item_id = item_id
        self.item_name = item_name
        self.price = price
        self.category = category
        self.is_available = True

    def __repr__(self):
        return f"{self.item_name} (Rs. {self.price:.2f})"

class Menu:
    """Aggregation relationship with FoodItem."""
    def __init__(self, menu_id: int):
        self.menu_id = menu_id
        self.items: List[FoodItem] = []

    def add_item(self, item: FoodItem):
        self.items.append(item)

    def remove_item(self, item_id: int):
        self.items = [it for it in self.items if it.item_id != item_id]

    def display_menu(self):
        print(f"\n--- Menu (ID: {self.menu_id}) ---")
        for it in self.items:
            status = "Available" if it.is_available else "Out of Stock"
            print(f"  [{it.item_id}] {it.item_name} - Rs. {it.price:.2f} ({it.category}) [{status}]")

class Restaurant:
    """Composition relationship with Menu."""
    def __init__(self, restaurant_id: int, name: str, location: str, rating: float):
        self.restaurant_id = restaurant_id
        self.name = name
        self.location = location
        self.rating = rating
        self.menu = Menu(menu_id=restaurant_id * 10)

    def add_menu_item(self, item: FoodItem):
        self.menu.add_item(item)

    def update_order_status(self, order_id: int, new_status: str):
        print(f"[Restaurant: {self.name}] Order #{order_id} status updated to: '{new_status}'")

class Customer:
    def __init__(self, customer_id: int, name: str, phone: str, address: str):
        self.customer_id = customer_id
        self.name = name
        self.phone = phone
        self.address = address

    def browse_restaurants(self, restaurants: List[Restaurant]):
        print(f"\n[Customer: {self.name}] Browsing Available Restaurants:")
        for r in restaurants:
            print(f"  • {r.name} | Location: {r.location} | Rating: {r.rating}★")

    def place_order(self, order_id: int, items: List[FoodItem]) -> 'Order':
        order = Order(order_id, self.customer_id, items)
        print(f"\n[Customer: {self.name}] Placed Order #{order_id} with {len(items)} items. Total: Rs. {order.total_amount:.2f}")
        return order

class Order:
    def __init__(self, order_id: int, customer_id: int, items: List[FoodItem]):
        self.order_id = order_id
        self.customer_id = customer_id
        self.items = items
        self.order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status = "Created"
        self.total_amount = self.calculate_total()

    def calculate_total(self) -> float:
        return sum(it.price for it in self.items)

    def update_status(self, new_status: str):
        self.status = new_status
        print(f"[Order #{self.order_id}] Status -> {self.status}")

class Payment:
    def __init__(self, payment_id: int, order: Order, amount: float, method: str):
        self.payment_id = payment_id
        self.order = order
        self.amount = amount
        self.method = method
        self.status = "Pending"

    def make_payment(self) -> bool:
        print(f"\n[Payment #{self.payment_id}] Processing Rs. {self.amount:.2f} via {self.method}...")
        if self.amount >= self.order.total_amount:
            self.status = "Successful"
            self.order.update_status("Paid & Confirmed")
            print(f"[Payment #{self.payment_id}] Payment SUCCESSFUL.")
            return True
        else:
            self.status = "Failed"
            self.order.update_status("Payment Failed")
            print(f"[Payment #{self.payment_id}] Payment FAILED.")
            return False

class DeliveryAgent:
    def __init__(self, agent_id: int, name: str, phone: str, vehicle_no: str):
        self.agent_id = agent_id
        self.name = name
        self.phone = phone
        self.vehicle_no = vehicle_no
        self.is_available = True

    def accept_delivery(self, delivery: 'Delivery'):
        self.is_available = False
        delivery.assign_agent(self)
        print(f"[Delivery Agent: {self.name}] Accepted Delivery for Order #{delivery.order.order_id}. Vehicle: {self.vehicle_no}")

class Delivery:
    def __init__(self, delivery_id: int, order: Order, destination: str):
        self.delivery_id = delivery_id
        self.order = order
        self.destination = destination
        self.agent: Optional[DeliveryAgent] = None
        self.status = "Assigned"

    def assign_agent(self, agent: DeliveryAgent):
        self.agent = agent

    def update_status(self, new_status: str):
        self.status = new_status
        print(f"[Delivery #{self.delivery_id}] Live Status: {self.status} (Destination: {self.destination})")


def run_system_simulation():
    print("==================================================================")
    print("      ONLINE FOOD DELIVERY SYSTEM - UML MODEL EXECUTION           ")
    print("==================================================================")

    # 1. Initialize Restaurant with Menu and FoodItems
    spice_garden = Restaurant(101, "Spice Garden Restaurant", "Chennai Central", 4.6)
    spice_garden.add_menu_item(FoodItem(1, "Paneer Butter Masala", 240.00, "Main Course"))
    spice_garden.add_menu_item(FoodItem(2, "Butter Naan (2 pcs)", 60.00, "Breads"))
    spice_garden.add_menu_item(FoodItem(3, "Veg Dum Biryani", 190.00, "Rice"))
    spice_garden.add_menu_item(FoodItem(4, "Gulab Jamun (2 pcs)", 70.00, "Dessert"))

    # 2. Customer Interaction
    cust = Customer(1001, "Angulakshmi S", "+91-9876543210", "Saveetha Hostels, Chennai")
    cust.browse_restaurants([spice_garden])
    spice_garden.menu.display_menu()

    # 3. Create Order
    selected_items = [spice_garden.menu.items[0], spice_garden.menu.items[1], spice_garden.menu.items[3]]
    order1 = cust.place_order(5001, selected_items)

    # 4. Process Payment
    payment = Payment(9001, order1, order1.total_amount, "UPI / GPay")
    pay_success = payment.make_payment()

    if pay_success:
        spice_garden.update_order_status(order1.order_id, "Food Preparation in Progress")
        
        # 5. Delivery Handling
        agent = DeliveryAgent(201, "Ramesh Kumar", "+91-9123456789", "TN-09-AB-1234")
        delivery = Delivery(7001, order1, cust.address)
        agent.accept_delivery(delivery)
        
        # 6. Delivery Tracking
        delivery.update_status("Picked up from Spice Garden")
        delivery.update_status("Out for Delivery - 5 mins away")
        delivery.update_status("Order Delivered Successfully to Customer")
        order1.update_status("Completed")

    print("==================================================================")
    print("                 WORKFLOW SIMULATION COMPLETED                    ")
    print("==================================================================")

if __name__ == "__main__":
    run_system_simulation()
