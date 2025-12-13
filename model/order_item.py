# model/order_item.py

class OrderItem:
    """
    Pure data object
    CSV columns:
    bookID, orderID, quantity, price_at_sale, line_total
    """

    def __init__(
        self,
        book_id: str,
        order_id: str | None = None,
        quantity: int = 0,
        price_at_sale: float = 0.0,
        line_total: float = 0.0
    ):
        self.book_id = str(book_id)
        self.order_id = str(order_id) if order_id else None
        self.quantity = int(quantity)
        self.price_at_sale = float(price_at_sale)
        self.line_total = float(line_total)



    def to_dict(self):
        return {
            "bookID": self.book_id,
            "orderID": self.order_id,
            "quantity": self.quantity,
            "price_at_sale": self.price_at_sale,
            "line_total": self.line_total
        }