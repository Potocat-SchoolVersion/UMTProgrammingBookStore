# view/main_window.py
import tkinter as tk
from tkinter import ttk, messagebox

# Controllers
from controller.book_controller import BookController
from controller.order_controller import OrderController
from controller.sales_controller import SalesController

# Models/Repository
from model.book_repository import CSVBookRepository

# Views
from view.book_view import BooksView
from view.order_view import OrderView
from view.sales_view import SalesView

class BookstoreApp:
    """Main application"""
    
    def __init__(self, root, current_user):
        self.root = root
        self.current_user = current_user
        self.root.title("🏪 UMT Programming Bookstore")
        self.root.geometry("1000x700")
        
        # Initialize Repository & Controllers
        self.repository = CSVBookRepository()
        self.book_controller = BookController(self.repository)
        self.order_controller = OrderController(self.repository, current_user)
        self.sales_controller = SalesController(self.repository)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup main UI"""
        # Header
        header = ttk.Frame(self.root)
        header.pack(fill='x', pady=10)

        # Logout button (right side)
        logout_btn = ttk.Button(header, text="⏻ Exit System", command=self.quit)
        logout_btn.pack(side='right', padx=10)
        
        title = ttk.Label(header, text="🏪 UMT PROGRAMMING BOOKSTORE", 
                        font=('Arial', 20, 'bold'))
        title.pack()
        
        # Show logged in user
        user_info = ttk.Label(header, 
                            text=f"👤 {self.current_user.username} ({self.current_user.role.upper()})",
                            font=('Arial', 10))
        user_info.pack()
        
        # Notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create Views that EVERYONE can see
        self.books_view = BooksView(self.notebook, self.book_controller, self.current_user)
        self.order_view = OrderView(self.notebook, self.order_controller, self.on_order_complete)
        
        # Add tabs for everyone
        self.notebook.add(self.books_view, text="📚 Books")
        self.notebook.add(self.order_view, text="🛒 Orders")
        
        # Create Sales view ONLY for managers
        if self.current_user.is_manager():
            self.sales_view = SalesView(self.notebook, self.sales_controller)
            self.notebook.add(self.sales_view, text="📊 Sales")
            print(f"✓ Sales tab visible for manager: {self.current_user.username}")
        else:
            self.sales_view = None
            print(f"✓ Sales tab hidden for staff: {self.current_user.username}")
        
        # Footer
        footer = ttk.Label(self.root, 
                        text=f"© 2024 UMT Bookstore | Logged in as: {self.current_user.username}", 
                        font=('Arial', 8), foreground='gray')
        footer.pack(pady=5)
    
    def on_order_complete(self):
        """Callback when order is completed"""
        self.books_view.refresh_books()
        messagebox.showinfo("Success", "Order processed!\nInventory updated.")
    
    def quit(self):
        if messagebox.askyesno("Exit Confirmation", "Are you sure you want to exit the system?"):
            self.root.destroy()

    def run(self):
        """Run the application"""
        self.root.mainloop()
