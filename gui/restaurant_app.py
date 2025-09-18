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

    # ---------------- Layout ----------------
    def build_layout(self):
        top_frame = tk.Frame(self.root, pady=8)
        top_frame.pack(fill='x')
        tk.Label(top_frame, text="Restaurant Ordering System", font=("Arial", 20, "bold")).pack()

        main_frame = tk.Frame(self.root)
        main_frame.pack(fill='both', expand=True)

        left_frame = tk.Frame(main_frame, padx=5, pady=5, bd=2, relief='groove')
        left_frame.grid(row=0, column=0, sticky='nsew')
        center_frame = tk.Frame(main_frame, padx=5, pady=5, bd=2, relief='groove')
        center_frame.grid(row=0, column=1, sticky='nsew')
        right_frame = tk.Frame(main_frame, padx=5, pady=5, bd=2, relief='groove')
        right_frame.grid(row=0, column=2, sticky='nsew')

        main_frame.columnconfigure(0, weight=2)
        main_frame.columnconfigure(1, weight=3)
        main_frame.columnconfigure(2, weight=2)
        main_frame.rowconfigure(0, weight=1)

        # Left: categories and menu list
        cat_frame = tk.Frame(left_frame)
        cat_frame.pack(fill='x', pady=(0, 5))
        tk.Label(cat_frame, text="Categories:").pack(anchor='w')
        # Category buttons are placeholders; product records currently have no category metadata.
        for cat in ["All"]:
            tk.Button(cat_frame, text=cat, width=10, command=lambda c=cat: self.filter_category(c)).pack(side='left', padx=2)

        menu_frame = tk.Frame(left_frame)
        menu_frame.pack(fill='both', expand=True)
        self.menu_tree = ttk.Treeview(menu_frame, columns=("id", "name", "price", "stock"), show='headings', height=12)
        for col, text, w in [("id", "ID", 40), ("name", "Name", 140), ("price", "Price", 70), ("stock", "Stock", 60)]:
            self.menu_tree.heading(col, text=text)
            self.menu_tree.column(col, width=w, anchor='center')
        self.menu_tree.pack(side='left', fill='both', expand=True)
        menu_scroll = ttk.Scrollbar(menu_frame, orient='vertical')
        menu_scroll.config(command=self.menu_tree.yview)  # type: ignore[arg-type]
        self.menu_tree.configure(yscrollcommand=menu_scroll.set)
        menu_scroll.pack(side='right', fill='y')

        qty_frame = tk.Frame(left_frame, pady=5)
        qty_frame.pack(fill='x')
        tk.Label(qty_frame, text="Qty:").pack(side='left')
        self.quantity_entry = tk.Entry(qty_frame, width=5)
        self.quantity_entry.insert(0, "1")
        self.quantity_entry.pack(side='left', padx=4)
        tk.Button(qty_frame, text="Add to Order", command=self.add_to_order).pack(side='left', padx=10)

