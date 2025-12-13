import tkinter as tk
from tkinter import ttk
from view.base_view import BaseView

class BooksView(BaseView):
    """View for displaying books"""
    
    def __init__(self, parent, book_controller, current_user):
        self.book_controller = book_controller  # <-- Store it first
        self.current_user = current_user
        super().__init__(parent, book_controller)  # <-- Then pass to parent
    
    def setup_ui(self):
        # Title
        title = ttk.Label(self, text="📚 Book Inventory", font=('Arial', 16, 'bold'))
        title.pack(pady=10)
        
        col_names = {
            'ID': 'Book ID',
            'Category': 'Category', 
            'Name': 'Book Name',
            'Price': 'Price (RM)',
            'Stock': 'Stock',
            'Sold': 'Sold'
        }
        
        # Filter frame
        filter_frame = ttk.Frame(self)
        filter_frame.pack(fill='x', padx=20, pady=5)
        
        ttk.Label(filter_frame, text="Filter by Category:").pack(side='left', padx=5)
        
        self.category_var = tk.StringVar(value="All")
        categories = self.book_controller.get_all_categories()
        category_combo = ttk.Combobox(filter_frame, textvariable=self.category_var, 
                                     values=categories, state='readonly', width=30)
        category_combo.pack(side='left', padx=5)
        category_combo.bind('<<ComboboxSelected>>', lambda e: self.refresh_books())
        
        ttk.Button(filter_frame, text="🔄 Refresh", command=self.refresh_books).pack(side='left', padx=5)
        
        # Treeview
        # Conditional columns based on role
        if self.current_user.is_manager():
            columns = ('ID', 'Category', 'Name', 'Price', 'Stock', 'Sold')
        else:  # Staff
            columns = ('ID', 'Category', 'Name', 'Price', 'Stock')  # <-- No 'Sold'

        self.tree = ttk.Treeview(self, columns=columns, show='headings', height=15)

        # Configure headings
        for col in columns:
            self.tree.heading(col, text=col_names[col])  
         # You'll need a mapping dict
        
        # Configure columns
        self.tree.heading('ID', text='Book ID')
        self.tree.heading('Category', text='Category')
        self.tree.heading('Name', text='Book Name')
        self.tree.heading('Price', text='Price (RM)')
        self.tree.heading('Stock', text='Stock')
        
        
        self.tree.column('ID', width=80)
        self.tree.column('Category', width=150)
        self.tree.column('Name', width=300)
        self.tree.column('Price', width=100)
        self.tree.column('Stock', width=80)
        

        if self.current_user.is_manager():
            self.tree.heading('Sold', text='Sold')
            self.tree.column('Sold', width=80)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True, padx=(20, 0), pady=10)
        scrollbar.pack(side='right', fill='y', padx=(0, 20), pady=10)
        
        self.refresh_books()
    
    def refresh_books(self):
        """Refresh book list from controller"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get books from controller
        category = self.category_var.get()
        books = self.book_controller.get_books_by_category(category)
        
        # Insert books  
        for book in books:
            if self.current_user.is_manager():
                values = (book.book_id, book.field, book.book_name, 
                        f"{book.price:.2f}", book.stock, book.sold)
            else:  # Staff - no sold column
                values = (book.book_id, book.field, book.book_name, 
                        f"{book.price:.2f}", book.stock)
            
            self.tree.insert('', 'end', values=values)
