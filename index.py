from sortedcontainers import SortedDict
from typing import Dict, Literal


class OrderBook:
    def __init__(self):
        self.orders: Dict[str, Dict[str, float]] = {}
        self.prices = {
            "BUY": SortedDict(),  # Lowest prices at the start
            "SELL": SortedDict(lambda x: -x)  # Highest prices at the start  
        }

    def add(self, id: str, order_type: Literal["BUY", "SELL"], price: float, quantity: int) -> None:
        if id in self.orders:
            print("Order with such id already exists")
            return
        
        self.orders[id] = {"type": order_type, "price": price}
        prices = self.prices[order_type]

        prices.setdefault(price, {})[id] = quantity
    
    def remove(self, id: str) -> None:
        if id not in self.orders:
            print("Order with such id does not exist")
            return
        
        order = self.orders[id]
        prices = self.prices[order["type"]]

        del prices[order["price"]][id]
        del self.orders[id]

        if not prices[order["price"]]:
            del prices[order["price"]]


ORDERS = [
    {"id": "001", "order": "Buy", "type": "Add", "price": 20.0, "quantity": 100},
    {"id": "002", "order": "Sell", "type": "Add", "price": 25.0, "quantity": 200},
    {"id": "003", "order": "Buy", "type": "Add", "price": 23.0, "quantity": 50},
    {"id": "004", "order": "Buy", "type": "Add", "price": 23.7, "quantity": 70},
    {"id": "003", "order": "Buy", "type": "Remove", "price": 23.0, "quantity": 50},
    {"id": "005", "order": "Sell", "type": "Add", "price": 28.0, "quantity": 100},
]

if __name__ == "__main__":
    order_book = OrderBook()

    for order in ORDERS:
        if order["type"] == "Add":
            order_book.add(order["id"], order["order"].upper(), order["price"], order["quantity"])
        else:
            order_book.remove(order["id"])

        print(f'Best BUY price is {order_book.prices["BUY"].peekitem(0)[0] if order_book.prices["BUY"] else "None"} and best SELL price is {order_book.prices["SELL"].peekitem(0)[0] if order_book.prices["SELL"] else "None"}')