# model/book.py
class Book:
    """Book entity - represents a single book"""
    
    def __init__(self, book_id, field, book_name, price, stock, sold):
        self.book_id = book_id
        self.field = field
        self.book_name = book_name
        self.price = float(price)
        self.stock = int(stock)
        self.sold = int(sold)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'bookID': self.book_id,
            'field': self.field,
            'bookName': self.book_name,
            'price': self.price,
            'stock': self.stock,
            'sold': self.sold
        }
    
    def has_sufficient_stock(self, quantity):
        """Check if book has enough stock"""
        return self.stock >= quantity
    
    def update_stock(self, quantity):
        """Update stock after sale"""
        self.stock -= quantity
        self.sold += quantity
    
    def calculate_revenue(self):
        """Calculate total revenue for this book"""
        return self.sold * self.price

