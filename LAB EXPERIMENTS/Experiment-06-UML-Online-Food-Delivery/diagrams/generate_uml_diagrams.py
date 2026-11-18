import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_class_diagram():
    fig, ax = plt.subplots(figsize=(12, 10), dpi=300)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 14)
    ax.axis('off')

    def draw_class(x, y, w, h, name, attrs, methods, bg='#F4F6F7', border='#2980B9'):
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0",
                                      facecolor=bg, edgecolor=border, linewidth=1.5)
        ax.add_patch(rect)
        # Title bar
        ax.plot([x, x + w], [y + h - 0.7, y + h - 0.7], color=border, linewidth=1.2)
        ax.text(x + w/2, y + h - 0.45, name, ha='center', va='center', fontsize=9.5, fontweight='bold', color='#1B4F72')
        # Attrs
        ay = y + h - 1.0
        for att in attrs:
            ax.text(x + 0.2, ay, att, fontsize=7.5, va='top', family='monospace')
            ay -= 0.35
        # Separator line
        div_y = y + h - 0.7 - len(attrs)*0.35 - 0.1
        ax.plot([x, x + w], [div_y, div_y], color=border, linewidth=1.0)
        # Methods
        my = div_y - 0.2
        for m in methods:
            ax.text(x + 0.2, my, m, fontsize=7.5, va='top', family='monospace')
            my -= 0.35

    # Classes placement
    # Row 1: Customer (left), Restaurant (middle), Menu (right)
    draw_class(0.8, 8.5, 4.0, 3.8, "Customer",
               ["- customerId: int", "- name: String", "- phone: String", "- address: String"],
               ["+ login(): bool", "+ browse(): List", "+ placeOrder(): Order", "+ makePayment(): bool"])

    draw_class(5.8, 8.5, 4.2, 3.8, "Restaurant",
               ["- restaurantId: int", "- name: String", "- location: String", "- rating: double"],
               ["+ manageMenu(): void", "+ updateOrderStatus(): void"])

    draw_class(11.0, 8.8, 4.2, 3.5, "Menu",
               ["- menuId: int", "- restaurantId: int"],
               ["+ addItem(item): void", "+ removeItem(id): void", "+ displayMenu(): void"])

    # FoodItem below Menu
    draw_class(11.0, 3.8, 4.2, 3.6, "FoodItem",
               ["- itemId: int", "- itemName: String", "- price: double", "- category: String", "- isAvailable: bool"],
               ["+ getDetails(): String"])

    # Row 2: Order (left), Payment (middle), Delivery (bottom middle), DeliveryAgent (bottom left)
    draw_class(0.8, 3.5, 4.0, 3.8, "Order",
               ["- orderId: int", "- customerId: int", "- orderDate: String", "- totalAmount: double", "- status: String"],
               ["+ createOrder(): void", "+ cancelOrder(): void", "+ calculateTotal(): double"])

    draw_class(5.8, 4.2, 4.2, 3.2, "Payment",
               ["- paymentId: int", "- orderId: int", "- amount: double", "- status: String"],
               ["+ makePayment(): void", "+ verifyPayment(): bool"])

    draw_class(0.8, 0.5, 4.0, 2.4, "DeliveryAgent",
               ["- agentId: int", "- name: String", "- vehicleNo: String"],
               ["+ acceptDelivery(): void", "+ updateStatus(): void"])

    draw_class(5.8, 0.5, 4.2, 2.8, "Delivery",
               ["- deliveryId: int", "- orderId: int", "- agentId: int", "- status: String"],
               ["+ trackLocation(): String", "+ completeDelivery(): void"])

    # Relationship connectors
    # Customer to Order (1 to *)
    ax.annotate('', xy=(2.8, 7.3), xytext=(2.8, 8.5), arrowprops=dict(arrowstyle='-', color='#1B4F72', lw=1.5))
    ax.text(3.0, 8.2, "1", fontsize=9, fontweight='bold')
    ax.text(3.0, 7.5, "*", fontsize=9, fontweight='bold')

    # Restaurant to Menu (Composition: filled diamond at Restaurant)
    ax.plot([10.0, 11.0], [10.4, 10.4], color='#1B4F72', lw=1.5)
    diamond = patches.Polygon([[10.0, 10.4], [10.25, 10.6], [10.5, 10.4], [10.25, 10.2]], facecolor='#1B4F72', edgecolor='#1B4F72')
    ax.add_patch(diamond)
    ax.text(10.6, 10.6, "owns 1", fontsize=8)

    # Menu to FoodItem (Aggregation: hollow diamond at Menu)
    ax.plot([13.1, 13.1], [8.8, 7.4], color='#1B4F72', lw=1.5)
    h_diamond = patches.Polygon([[13.1, 8.8], [13.3, 8.55], [13.1, 8.3], [12.9, 8.55]], facecolor='white', edgecolor='#1B4F72', lw=1.5)
    ax.add_patch(h_diamond)
    ax.text(13.3, 7.6, "1..*", fontsize=8, fontweight='bold')

    # Order to Payment (1 to 1)
    ax.plot([4.8, 5.8], [5.5, 5.5], color='#1B4F72', lw=1.5)
    ax.text(5.0, 5.7, "1", fontsize=8)
    ax.text(5.5, 5.7, "1", fontsize=8)

    # Order to Delivery (1 to 0..1)
    ax.plot([2.8, 2.8, 5.8], [3.5, 2.0, 2.0], color='#1B4F72', lw=1.5)
    ax.text(4.8, 2.2, "0..1", fontsize=8)

    # DeliveryAgent to Delivery (1 to *)
    ax.plot([4.8, 5.8], [1.7, 1.7], color='#1B4F72', lw=1.5)
    ax.text(5.0, 1.9, "1", fontsize=8)
    ax.text(5.5, 1.9, "*", fontsize=8)

    plt.title("UML Class Diagram: Online Food Delivery System\nSaveetha School of Engineering | CSA10 | Angulakshmi S (192524402)",
              fontsize=13, fontweight='bold', pad=15, color='#1B4F72')
    plt.tight_layout()
    plt.savefig(r"c:\Users\ANGULAKSHMI SUBBURAJ\Downloads\CSA1022-SOFTWARE-ENGINEERING\LAB EXPERIMENTS\Experiment-06-UML-Online-Food-Delivery\diagrams\class_diagram.png", dpi=300)
    plt.savefig(r"c:\Users\ANGULAKSHMI SUBBURAJ\Downloads\CSA1022-SOFTWARE-ENGINEERING\LAB EXPERIMENTS\Experiment-06-UML-Online-Food-Delivery\diagrams\class_diagram.svg")
    plt.close()
    print("Class diagram generated.")

def generate_use_case_diagram():
    fig, ax = plt.subplots(figsize=(12, 9), dpi=300)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 12)
    ax.axis('off')

    # System boundary
    rect = patches.Rectangle((3.8, 0.8), 6.4, 10.2, facecolor='#FDFEFE', edgecolor='#2C3E50', linewidth=2, linestyle='--')
    ax.add_patch(rect)
    ax.text(7.0, 10.6, "Online Food Delivery Platform", ha='center', fontsize=12, fontweight='bold', color='#2C3E50')

    # Use cases
    ucs = [
        ("Browse Restaurants", 9.6),
        ("View Menu & Food Items", 8.4),
        ("Place Food Order", 7.2),
        ("Make Online Payment", 6.0),
        ("Track Delivery Status", 4.8),
        ("Manage Restaurant Menu", 3.6),
        ("Update Order Status", 2.4),
        ("Accept Delivery Request", 1.4)
    ]

    for text, y in ucs:
        ell = patches.Ellipse((7.0, y), 4.2, 0.8, facecolor='#EBF5FB', edgecolor='#2980B9', linewidth=1.5)
        ax.add_patch(ell)
        ax.text(7.0, y, text, ha='center', va='center', fontsize=9, fontweight='bold', color='#1B4F72')

    def draw_actor(x, y, name):
        # Head
        c = patches.Circle((x, y), 0.25, facecolor='#FDEDEC', edgecolor='#C0392B', lw=1.5)
        ax.add_patch(c)
        # Body
        ax.plot([x, x], [y - 0.25, y - 0.8], color='#C0392B', lw=1.8)
        # Arms
        ax.plot([x - 0.35, x + 0.35], [y - 0.45, y - 0.45], color='#C0392B', lw=1.8)
        # Legs
        ax.plot([x, x - 0.3], [y - 0.8, y - 1.3], color='#C0392B', lw=1.8)
        ax.plot([x, x + 0.3], [y - 0.8, y - 1.3], color='#C0392B', lw=1.8)
        ax.text(x, y - 1.6, name, ha='center', fontsize=10, fontweight='bold', color='#78281F')

    # Actors
    draw_actor(1.8, 8.5, "Customer")
    draw_actor(12.2, 5.0, "Restaurant")
    draw_actor(12.2, 2.0, "Delivery Agent")

    # Connect Customer
    for y in [9.6, 8.4, 7.2, 6.0, 4.8]:
        ax.plot([2.1, 4.9], [8.0, y], color='#7F8C8D', lw=1.2)

    # Connect Restaurant
    for y in [3.6, 2.4]:
        ax.plot([11.8, 9.1], [4.5, y], color='#7F8C8D', lw=1.2)

    # Connect Delivery Agent
    for y in [2.4, 1.4]:
        ax.plot([11.8, 9.1], [1.7, y], color='#7F8C8D', lw=1.2)

    plt.title("UML Use Case Diagram: Online Food Delivery System\nSaveetha School of Engineering | CSA10 | Angulakshmi S (192524402)",
              fontsize=13, fontweight='bold', pad=15, color='#1B4F72')
    plt.tight_layout()
    plt.savefig(r"c:\Users\ANGULAKSHMI SUBBURAJ\Downloads\CSA1022-SOFTWARE-ENGINEERING\LAB EXPERIMENTS\Experiment-06-UML-Online-Food-Delivery\diagrams\use_case_diagram.png", dpi=300)
    plt.savefig(r"c:\Users\ANGULAKSHMI SUBBURAJ\Downloads\CSA1022-SOFTWARE-ENGINEERING\LAB EXPERIMENTS\Experiment-06-UML-Online-Food-Delivery\diagrams\use_case_diagram.svg")
    plt.close()
    print("Use Case diagram generated.")

def generate_activity_diagram():
    fig, ax = plt.subplots(figsize=(8, 12), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 14)
    ax.axis('off')

    def draw_action(y, text, bg='#EAFAF1', border='#27AE60'):
        r = patches.FancyBboxPatch((2.2, y - 0.35), 5.6, 0.7, boxstyle="round,pad=0.2,rounding_size=0.35",
                                   facecolor=bg, edgecolor=border, lw=1.5)
        ax.add_patch(r)
        ax.text(5.0, y, text, ha='center', va='center', fontsize=9, fontweight='bold', color='#145A32')

    def draw_arrow(y1, y2, x=5.0):
        ax.annotate('', xy=(x, y2), xytext=(x, y1),
                    arrowprops=dict(facecolor='#2C3E50', edgecolor='#2C3E50', width=1.5, headwidth=6, headlength=6))

    # Initial Node
    c = patches.Circle((5.0, 13.2), 0.25, facecolor='#2C3E50', edgecolor='#2C3E50')
    ax.add_patch(c)
    draw_arrow(12.95, 12.45)

    # Actions
    draw_action(12.1, "1. Browse Restaurants & View Menu")
    draw_arrow(11.75, 11.05)

    draw_action(10.7, "2. Select Food Items & Add to Cart")
    draw_arrow(10.35, 9.65)

    draw_action(9.3, "3. Place Order & Proceed to Payment")
    draw_arrow(8.95, 8.25)

    # Decision: Payment Success?
    d = patches.Polygon([[5.0, 8.25], [6.5, 7.65], [5.0, 7.05], [3.5, 7.65]], facecolor='#FDEDEC', edgecolor='#C0392B', lw=1.5)
    ax.add_patch(d)
    ax.text(5.0, 7.65, "Payment\nSuccess?", ha='center', va='center', fontsize=8, fontweight='bold', color='#78281F')

    # No -> Cancel
    ax.plot([3.5, 1.2, 1.2], [7.65, 7.65, 6.0], color='#C0392B', lw=1.5)
    ax.text(2.2, 7.8, "[No]", fontsize=8, fontweight='bold', color='#C0392B')
    r_fail = patches.FancyBboxPatch((0.2, 5.3), 2.0, 0.7, boxstyle="round,pad=0.1", facecolor='#FADBD8', edgecolor='#C0392B', lw=1.2)
    ax.add_patch(r_fail)
    ax.text(1.2, 5.65, "Payment Failed\nOrder Cancelled", ha='center', va='center', fontsize=7.5, fontweight='bold')
    # Final node for failure
    ax.plot([1.2, 1.2], [5.3, 4.5], color='#C0392B', lw=1.2)
    c_out1 = patches.Circle((1.2, 4.2), 0.22, facecolor='none', edgecolor='#2C3E50', lw=1.5)
    c_in1 = patches.Circle((1.2, 4.2), 0.12, facecolor='#2C3E50')
    ax.add_patch(c_out1); ax.add_patch(c_in1)

    # Yes -> Restaurant confirms
    draw_arrow(7.05, 6.25)
    ax.text(5.15, 6.65, "[Yes]", fontsize=8, fontweight='bold', color='#27AE60')

    draw_action(5.9, "4. Restaurant Confirms Order & Prepares Food")
    draw_arrow(5.55, 4.85)

    draw_action(4.5, "5. System Assigns Delivery Agent")
    draw_arrow(4.15, 3.45)

    draw_action(3.1, "6. Agent Picks up Food & Delivers to Address")
    draw_arrow(2.75, 2.05)

    draw_action(1.7, "7. Order Delivered & Receipt Generated")
    draw_arrow(1.35, 0.75)

    # Final Node
    c_out = patches.Circle((5.0, 0.5), 0.25, facecolor='none', edgecolor='#2C3E50', lw=1.8)
    c_in = patches.Circle((5.0, 0.5), 0.14, facecolor='#2C3E50')
    ax.add_patch(c_out); ax.add_patch(c_in)

    plt.title("UML Activity Diagram: Online Food Delivery Workflow\nSaveetha School of Engineering | CSA10 | Angulakshmi S (192524402)",
              fontsize=12, fontweight='bold', pad=15, color='#1B4F72')
    plt.tight_layout()
    plt.savefig(r"c:\Users\ANGULAKSHMI SUBBURAJ\Downloads\CSA1022-SOFTWARE-ENGINEERING\LAB EXPERIMENTS\Experiment-06-UML-Online-Food-Delivery\diagrams\activity_diagram.png", dpi=300)
    plt.savefig(r"c:\Users\ANGULAKSHMI SUBBURAJ\Downloads\CSA1022-SOFTWARE-ENGINEERING\LAB EXPERIMENTS\Experiment-06-UML-Online-Food-Delivery\diagrams\activity_diagram.svg")
    plt.close()
    print("Activity diagram generated.")

if __name__ == "__main__":
    generate_class_diagram()
    generate_use_case_diagram()
    generate_activity_diagram()
