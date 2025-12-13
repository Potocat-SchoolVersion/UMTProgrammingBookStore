# controller/order_controller.py
from model.order import Order
from model.order_item import OrderItem
from model.discount import Discount
from tools.file_handler import append_save_file

import uuid
from datetime import datetime


class OrderController:
    """Controller for order operations"""

    ORDERS_FIELDS = ["order_id", "date_time", "staff_id", "subtotal", "discount", "tax", "total"]
    ORDER_ITEMS_FIELDS = ["bookID", "orderID", "quantity", "price_at_sale", "line_total"]

    def __init__(self, repository, current_user):
        self.repository = repository
        self.current_user = current_user  # keep for staff_id + new orders
        self.order = self.create_new_order(current_user)
        self.order_item_list = []

    def create_new_order(self, current_user):
        order_id = self.new_id()
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return Order(
            order_id=order_id,
            date_time=date_time,
            staff_id=current_user.staff_id,
            subtotal=0.0,
            discount=0.0,
            tax=0.0,
            total=0.0
        )

    def reset_order(self):
        """Start a fresh order + empty cart."""
        self.order = self.create_new_order(self.current_user)
        self.order_item_list = []

    def add_item_to_order(self, book, quantity: int):
        quantity = int(quantity)

        # Merge: if same book already exists in cart, update it instead of new line
        for item in self.order_item_list:
            if item.book_id.upper() == book.book_id.upper():
                item.quantity += quantity
                item.line_total = item.quantity * item.price_at_sale
                return

        item = OrderItem(
            book_id=book.book_id,
            order_id=self.order.order_id,
            quantity=quantity,
            price_at_sale=book.price,
            line_total=quantity * book.price
        )
        self.order_item_list.append(item)

    def calculate_order(self, discount_voucher: str = ""):
        """Fill self.order subtotal/discount/tax/total based on current cart."""
        self.order.subtotal = sum(float(item.line_total) for item in self.order_item_list)

        discount_rate = Discount.get_discount_rate(discount_voucher)
        self.order.discount = self.order.subtotal * float(discount_rate)

        after_discount = self.order.subtotal - self.order.discount
        self.order.tax = after_discount * float(self.get_tax_rate())
        self.order.total = after_discount + self.order.tax

        return Discount.get_discount_text(discount_voucher)

    def commit_order(self, discount_voucher: str, cash_received: float):
        """
        Commit transaction:
        - calculate totals
        - validate cash
        - update stock
        - append to CSV
        Returns a dict you can use for receipt / UI.
        """
        if not self.order_item_list:
            return False, "Cart is empty!", None

        # Validate voucher (Discount methods may throw if invalid)
        try:
            discount_text = self.calculate_order(discount_voucher.strip().upper())
        except Exception:
            return False, "Invalid voucher code!", None

        total = float(self.order.total)

        # Validate cash
        try:
            cash = float(cash_received)
        except ValueError:
            return False, "Cash received must be a number.", None

        if cash < total:
            return False, f"Insufficient cash. Need RM{total:.2f}", None

        balance = cash - total

        # Update inventory (commit stock changes)
        # NOTE: your repository.update_stock already checks sufficient stock.
        for item in self.order_item_list:
            ok = self.repository.update_stock(item.book_id, int(item.quantity))
            if not ok:
                return False, f"Stock update failed for Book ID {item.book_id}", None

        # Append to CSV
        self.append_order_to_csv()
        self.append_order_items_to_csv()

        receipt = {
            "order_id": self.order.order_id,
            "date_time": self.order.date_time,
            "staff_id": self.order.staff_id,
            "items": [
                {
                    "bookID": it.book_id,
                    "quantity": int(it.quantity),
                    "price_at_sale": float(it.price_at_sale),
                    "line_total": float(it.line_total),
                }
                for it in self.order_item_list
            ],
            "subtotal": float(self.order.subtotal),
            "voucher": discount_voucher.strip().upper(),
            "discount_text": discount_text,
            "discount": float(self.order.discount),
            "tax": float(self.order.tax),
            "total": float(self.order.total),
            "cash_received": float(cash),
            "balance": float(balance),
        }

        # Start fresh order after commit
        self.reset_order()

        return True, "Order committed!", receipt

    @staticmethod
    def get_tax_rate():
        return 0.06

    @staticmethod
    def new_id() -> str:
        return uuid.uuid4().hex

    def append_order_to_csv(self):
        append_save_file(
            filename="order",
            file_type="csv",
            fieldnames=self.ORDERS_FIELDS,
            datas=[self.order]
        )

    def append_order_items_to_csv(self):
        append_save_file(
            filename="order_item",
            file_type="csv",
            fieldnames=self.ORDER_ITEMS_FIELDS,
            datas=self.order_item_list
        )
