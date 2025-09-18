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

        # Center: order tree, buttons and totals
        tk.Label(center_frame, text="Current Order", font=("Arial", 14, "bold")).pack(anchor='w')
        order_tree_frame = tk.Frame(center_frame)
        order_tree_frame.pack(fill='both', expand=True)
        self.order_tree = ttk.Treeview(order_tree_frame, columns=("name", "qty", "price", "subtotal"), show='headings', height=14)
        self.order_tree.heading("name", text="Item")
        self.order_tree.heading("qty", text="Qty")
        self.order_tree.heading("price", text="Price")
        self.order_tree.heading("subtotal", text="Subtotal")
        self.order_tree.column("name", width=140)
        self.order_tree.column("qty", width=40, anchor='center')
        self.order_tree.column("price", width=70, anchor='e')
        self.order_tree.column("subtotal", width=90, anchor='e')
        self.order_tree.pack(side='left', fill='both', expand=True)
        order_scroll = ttk.Scrollbar(order_tree_frame, orient='vertical')
        order_scroll.config(command=self.order_tree.yview)  # type: ignore[arg-type]
        self.order_tree.configure(yscrollcommand=order_scroll.set)
        order_scroll.pack(side='right', fill='y')

        btn_frame = tk.Frame(center_frame, pady=5)
        btn_frame.pack(fill='x')
        tk.Button(btn_frame, text="Remove Last Item", command=self.remove_last_item).pack(side='left')
        tk.Button(btn_frame, text="Checkout", command=self.checkout_popup).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Print Receipt", command=self.print_receipt).pack(side='left')

        totals_frame = tk.Frame(center_frame, pady=5)
        totals_frame.pack(fill='x')
        tk.Label(totals_frame, textvariable=self.subtotal_var).pack(anchor='e')
        tk.Label(totals_frame, textvariable=self.tax_var).pack(anchor='e')
        tk.Label(totals_frame, textvariable=self.total_var, font=("Arial", 12, "bold")).pack(anchor='e')

        # Right: stock levels and actions
        tk.Label(right_frame, text="Stock Levels", font=("Arial", 14, "bold")).pack(anchor='w')
        stock_frame = tk.Frame(right_frame)
        stock_frame.pack(fill='both', expand=True)
        self.stock_tree = ttk.Treeview(stock_frame, columns=("id", "name", "stock"), show='headings', height=12)
        self.stock_tree.heading("id", text="ID")
        self.stock_tree.heading("name", text="Name")
        self.stock_tree.heading("stock", text="Stock")
        self.stock_tree.column("id", width=40, anchor='center')
        self.stock_tree.column("name", width=140)
        self.stock_tree.column("stock", width=60, anchor='center')
        self.stock_tree.pack(side='left', fill='both', expand=True)
        stock_scroll = ttk.Scrollbar(stock_frame, orient='vertical')
        stock_scroll.config(command=self.stock_tree.yview)  # type: ignore[arg-type]
        self.stock_tree.configure(yscrollcommand=stock_scroll.set)
        stock_scroll.pack(side='right', fill='y')

        self.stock_tree.tag_configure('low', background='#ffcccc')
        self.stock_tree.tag_configure('ok', background='#ccffcc')

        right_btns = tk.Frame(right_frame, pady=5)
        right_btns.pack(fill='x')
        tk.Button(right_btns, text="Send to Kitchen", command=self.send_to_kitchen).pack(fill='x', pady=2)
        tk.Button(right_btns, text="Hold Order", command=self.hold_order).pack(fill='x', pady=2)
        tk.Button(right_btns, text="Cancel Order", command=self.cancel_order).pack(fill='x', pady=2)
        tk.Button(right_btns, text="Load Menu", command=self.reload_menu).pack(fill='x', pady=2)
        tk.Button(right_btns, text="Update Stock", command=self.update_stock_placeholder).pack(fill='x', pady=2)

    # --------------- Product / Stock ---------------
    def refresh_products(self):
        if not self.inventory.products:
            # Use updated loader compatible with group project database format
            load_method = getattr(self.inventory, 'load', None)
            if callable(load_method):
                load_method()
        if not self.menu_tree:
            return
        for row in self.menu_tree.get_children():
            self.menu_tree.delete(row)
        for p in self.inventory.products:
            # Category filtering skipped (no category field). Could be extended later.
            self.menu_tree.insert('', 'end', values=(getattr(p, 'prodID', getattr(p, 'id', '?')),
                                                     getattr(p, 'prodName', 'Unknown'),
                                                     f"${getattr(p, 'price', getattr(p, 'prodPrice', 0.0)):.2f}",
                                                     getattr(p, 'stock', getattr(p, 'prodStock', 0))))

    def refresh_stock_display(self):
        if not self.stock_tree:
            return
        for row in self.stock_tree.get_children():
            self.stock_tree.delete(row)
        for p in self.inventory.products:
            stock_val = getattr(p, 'stock', getattr(p, 'prodStock', 0))
            tag = 'low' if stock_val <= 5 else 'ok'
            self.stock_tree.insert('', 'end', values=(getattr(p, 'prodID', getattr(p, 'id', '?')),
                                                      getattr(p, 'prodName', 'Unknown'),
                                                      stock_val), tags=(tag,))

    def filter_category(self, category: str):
        self.current_category = None if category == 'All' else category
        self.refresh_products()

    # --------------- Order Logic ---------------
    def add_to_order(self):
        if not self.menu_tree:
            return
        selection = self.menu_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a menu item first.")
            return
        try:
            assert self.quantity_entry is not None, "Quantity entry not initialized"
            qty = int(self.quantity_entry.get())
            if qty <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Bad Quantity", "Enter a positive whole number for quantity.")
            return
        item_vals = self.menu_tree.item(selection[0], 'values')
        pid = int(item_vals[0])
        product = self.inventory.get_product(pid)
        if not product:
            messagebox.showerror("Error", "Product not found.")
            return
        current_stock = getattr(product, 'stock', getattr(product, 'prodStock', 0))
        if current_stock < qty:
            messagebox.showinfo("Out of Stock", f"Only {current_stock} left in stock.")
            return
        self.order.add_item(product, qty)
        self.update_order_tree()
        self.update_order_summary()

    def update_order_tree(self):
        if not self.order_tree:
            return
        for row in self.order_tree.get_children():
            self.order_tree.delete(row)
        for p, q in self.order.items:
            price_val = getattr(p, 'price', getattr(p, 'prodPrice', 0.0))
            name_val = getattr(p, 'prodName', getattr(p, 'addonName', 'Item'))
            subtotal = price_val * q
            self.order_tree.insert('', 'end', values=(name_val, q, f"${price_val:.2f}", f"${subtotal:.2f}"))

    def remove_last_item(self):
        self.order.remove_last_item()
        self.update_order_tree()
        self.update_order_summary()

    def update_order_summary(self):
        subtotal = self.order.total()
        tax = subtotal * self.TAX_RATE
        total = subtotal + tax
        self.subtotal_var.set(f"Subtotal: ${subtotal:.2f}")
        self.tax_var.set(f"Tax: ${tax:.2f}")
        self.total_var.set(f"Total: ${total:.2f}")
