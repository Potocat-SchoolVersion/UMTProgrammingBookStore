import tkinter as tk
from tkinter import ttk, messagebox

# Controllers
from controller.staff_controller import StaffController
from controller.book_controller import BookController
from controller.order_controller import OrderController
from controller.sales_controller import SalesController

# Models/Repository
from model.book_repository import CSVBookRepository

# Views
from view.login_view import LoginView
from view.book_view import BooksView
from view.order_view import OrderView
from view.sales_view import SalesView


def launch_bookstore(staff):
    """Launch bookstore app after successful login"""
    root = tk.Tk()
    app = BookstoreApp(root, staff)
    app.run()


if __name__ == "__main__":
    # Initialize staff controller
    staff_controller = StaffController()
    
    # Show login screen
    login_root = tk.Tk()
    login_view = LoginView(login_root, staff_controller, launch_bookstore)
    login_root.mainloop()
