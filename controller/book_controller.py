# controller/book_controller.py
from model.book_repository import bookStorage

class BookController:
    """Controller for book operations"""
    
    def __init__(self, repository):
        self.repository = repository
    
    def get_all_books(self):
        """Get all books"""
        self.repository.load_books()
        return self.repository.get_all_books()
    
    def get_books_by_category(self, category):
        """Get books filtered by category"""
        self.repository.load_books()
        if category == "All":
            return self.repository.get_all_books()
        return self.repository.get_books_by_field(category)
    
    def get_all_categories(self):
        """Get all categories"""
        return ["All"] + self.repository.get_all_fields()
    
    def search_book(self, book_id):
        """Search for a book by ID"""
        return self.repository.get_book_by_id(book_id)
