# model/order.py

class Order:
    """
    Pure data object
    CSV columns:
    order_id, date_time, staff_id, subtotal, discount, tax, total
    """

    def __init__(
        self,
        order_id: str | None = None,
        date_time: str | None = None,
        staff_id: str | None = None,
        subtotal: float = 0.0,
        discount: float = 0.0,
        tax: float = 0.0,
        total: float = 0.0
    ):
        self.order_id = str(order_id) if order_id else None
        self.date_time = date_time          # controller must supply this
        self.staff_id = str(staff_id) if staff_id else None

        self.subtotal = float(subtotal)
        self.discount = float(discount)
        self.tax = float(tax)
        self.total = float(total)



    def to_dict(self):
        return {
            "order_id": self.order_id,
            "date_time": self.date_time,
            "staff_id": self.staff_id,
            "subtotal": self.subtotal,
            "discount": self.discount,
            "tax": self.tax,
            "total": self.total
        }
