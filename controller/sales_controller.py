from model.book import Book

class SalesController:
    """sales analytics"""
    
    def __init__(self, repository):
        self.repository = repository
    
    def get_sales_summary(self):
        """Get sales summary"""
        self.repository.load_books()
        books = self.repository.get_all_books()
        
        total_sold = sum(book.sold for book in books)
        total_revenue = sum(book.calculate_revenue() for book in books)
        
        return {
            'books': books,
            'total_sold': total_sold,
            'total_revenue': total_revenue
        }
    
    def get_top_sellers(self, limit=5):
        """Get top selling books"""
        self.repository.load_books()
        books = self.repository.get_all_books()
        sorted_books = sorted(books, key=lambda x: x.sold, reverse=True)
        return sorted_books[:limit]
    
    def get_highest_revenue(self, limit=5):
        """Get highest revenue books"""
        self.repository.load_books()
        books = self.repository.get_all_books()
        book_revenue = [(book, book.calculate_revenue()) for book in books]
        sorted_books = sorted(book_revenue, key=lambda x: x[1], reverse=True)
        return sorted_books[:limit]

    
    def get_low_stock_books(self, threshold=20):
        """Get books with low stock"""
        self.repository.load_books()
        books = self.repository.get_all_books()
        return [book for book in books if book.stock < threshold]
