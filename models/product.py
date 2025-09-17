"""Product model, expand if needed."""
from dataclasses import dataclass

@dataclass
class Product:
    pid: int
    name: str
    price: float
    stock: int
    category: str  
