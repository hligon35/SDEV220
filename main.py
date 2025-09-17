"""Main entry point."""
from gui.restaurant_app import RestaurantApp
from models import Inventory
import tkinter as tk

def main():
    inv = Inventory()
    inv.load_products()
    root = tk.Tk()
    app = RestaurantApp(root, inv) 
    root.minsize(1050, 600)
    root.mainloop()

if __name__ == "__main__":
    main()
