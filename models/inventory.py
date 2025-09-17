"""Inventory stub class."""
from __future__ import annotations
from typing import List, Optional
import os
from .product import Product

class Inventory:
    def __init__(self, filename: str = "inventory.txt"):
        self.filename = filename
        self.products: List[Product] = []

    def load_products(self):
        """Upload using inventory file
        """
        self.products.clear()
        if not os.path.exists(self.filename):
            return
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    parts = line.split('|')
                    if len(parts) != 5:
                        continue
                    pid, name, price, stock, category = parts
                    try:
                        self.products.append(Product(int(pid), name, float(price), int(stock), category))
                    except ValueError:
                        continue
        except Exception as e:
            print("Problem reading inventory file:", e)

    def save_products(self):
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                for p in self.products:
                    f.write(f"{p.pid}|{p.name}|{p.price}|{p.stock}|{p.category}\n")
        except Exception as e:
            print("Could not save inventory:", e)

    def get_product(self, pid: int) -> Optional[Product]:
        for p in self.products:
            if p.pid == pid:
                return p
        return None

    def get_stock(self, pid: int) -> int:
        prod = self.get_product(pid)
        return prod.stock if prod else 0

    def reduce_stock(self, pid: int, qty: int):
        prod = self.get_product(pid)
        if prod and prod.stock >= qty:
            prod.stock -= qty
            return True
        return False