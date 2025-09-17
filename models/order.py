"""Order stub class."""
from __future__ import annotations
from typing import List, Tuple
from .product import Product

class Order:
    def __init__(self):
        self.items: List[Tuple[Product, int]] = []

    def add_item(self, product: Product, qty: int):
        self.items.append((product, qty))

    def remove_last_item(self):
        if self.items:
            self.items.pop()

    def total(self) -> float:
        return sum(p.price * q for p, q in self.items)

    def summary(self) -> str:
        lines = ["Receipt Summary:"]
        for p, q in self.items:
            lines.append(f"{p.name} x{q} @ ${p.price:.2f} = ${p.price * q:.2f}")
        lines.append("-" * 28)
        lines.append(f"Subtotal: ${self.total():.2f}")
        return "\n".join(lines)
