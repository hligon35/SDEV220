"""RestaurantApp GUI.

Heads-up:
- Products expose prodID/prodName/prodPrice/prodStock (aliases: id/price/stock).
- Inventory.load() pulls products + addons, but we only list products for now.
- Order items could be a Product or an Addon; UI sticks to products until we expand it.

Category buttons are just filler (no category field yet). 'All' just reloads everything.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional

from models import Inventory, Order

class RestaurantApp:
    TAX_RATE = 0.07

    def __init__(self, root: tk.Tk, inventory: Inventory):
        self.root = root
        self.root.title("Restaurant Ordering System")
        self.inventory = inventory
        self.order = Order()
        self.current_category: Optional[str] = None

        # Declare widget attributes for type checking
        self.menu_tree = None
        self.order_tree = None
        self.stock_tree = None
        self.quantity_entry = None

        self.subtotal_var = tk.StringVar(value="Subtotal: $0.00")
        self.tax_var = tk.StringVar(value="Tax: $0.00")
        self.total_var = tk.StringVar(value="Total: $0.00")

        self.build_layout()
        # Initial population
        self.refresh_products()
        self.refresh_stock_display()
        self.update_order_summary()

