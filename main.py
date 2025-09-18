"""Main entry point integrating with group project database format.

Currently this does NOT launch the old GUI (excluded by repo policy). Instead it:
  - Loads products and addons via the enhanced Inventory class
  - Prints a brief summary to stdout

Hook a GUI or CLI menu here later as needed.
"""
from models import Inventory, Order


def main():
    inv = Inventory()
    inv.load()
    print(f"Loaded {len(inv.products)} products and {len(inv.addons)} addons.")
    if inv.products:
        first = inv.products[0]
        print("First product:", first.prodName, "Price:", first.prodPrice)
    # Simple order demo
    order = Order()
    if inv.products:
        order.add_item(inv.products[0], 2)
    if inv.addons:
        order.add_item(inv.addons[0], 1)
    print(order.summary())


if __name__ == "__main__":
    main()
