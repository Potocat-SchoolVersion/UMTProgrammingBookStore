import tkinter as tk
from tkinter import ttk, messagebox

class LoginView:
    """Login screen view"""
    
    def __init__(self, root, staff_controller, on_login_success):
        self.root = root
        self.staff_controller = staff_controller
        self.on_login_success = on_login_success
        
        self.root.title("UMT Bookstore - Login")
        self.root.geometry("400x450")
        self.root.resizable(False, False)
        
        # Set background color to see layout
        self.root.configure(bg='white')
        
        self.setup_ui()
        self.center_window()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        """Setup login UI"""
        # Main container with white background
        container = tk.Frame(self.root, bg='white')
        container.pack(fill='both', expand=True, padx=40, pady=40)
        
        # Logo
        logo = tk.Label(container, text="🏪", font=('Arial', 50), bg='white')
        logo.pack(pady=(0, 10))
        
        # Title
        title = tk.Label(container, text="UMT BOOKSTORE", 
                        font=('Arial', 20, 'bold'), bg='white')
        title.pack()
        
        # Subtitle
        subtitle = tk.Label(container, text="Please login to continue", 
                           font=('Arial', 10), bg='white', fg='gray')
        subtitle.pack(pady=(5, 30))
        
        # Staff ID Label
        id_label = tk.Label(container, text="Staff ID:", 
                           font=('Arial', 10), bg='white', anchor='w')
        id_label.pack(fill='x')
        
        # Staff ID Entry
        self.staff_id_var = tk.StringVar()
        staff_id_entry = tk.Entry(container, textvariable=self.staff_id_var, 
                                  font=('Arial', 11), relief='solid', bd=1)
        staff_id_entry.pack(fill='x', pady=(5, 15), ipady=5)
        staff_id_entry.focus()
        
        # Password Label
        pw_label = tk.Label(container, text="Password:", 
                           font=('Arial', 10), bg='white', anchor='w')
        pw_label.pack(fill='x')
        
        # Password Entry
        self.password_var = tk.StringVar()
        password_entry = tk.Entry(container, textvariable=self.password_var, 
                                 show="●", font=('Arial', 11), relief='solid', bd=1)
        password_entry.pack(fill='x', pady=(5, 25), ipady=5)
        
        # LOGIN BUTTON - With explicit styling
        login_button = tk.Button(
            container,
            text="LOGIN",
            command=self.handle_login,
            font=('Arial', 12, 'bold'),
            bg='#4CAF50',
            fg='white',
            relief='flat',
            cursor='hand2',
            activebackground='#45a049',
            activeforeground='white'
        )
        login_button.pack(fill='x', ipady=10)
        
        # Make button visible with force update
        login_button.update()
        
        # Bind Enter key
        staff_id_entry.bind('<Return>', lambda e: password_entry.focus())
        password_entry.bind('<Return>', lambda e: self.handle_login())
        
        # Test info
        info_text = "Test Accounts:\nManager: admin / admin\nStaff: S001 / 12345678"
        info = tk.Label(container, text=info_text, font=('Arial', 8), 
                       bg='white', fg='gray', justify='center')
        info.pack(pady=(20, 0))
        
        print("✓ Login button created and packed!")  # Debug message
    
    def handle_login(self):
        """Handle login"""
        print("Login button clicked!")  # Debug message
        
        staff_id = self.staff_id_var.get().strip()
        password = self.password_var.get()
        
        if not staff_id:
            messagebox.showerror("Error", "Please enter Staff ID")
            return
        
        if not password:
            messagebox.showerror("Error", "Please enter Password")
            return
        
        # Attempt login
        role, logged_in = self.staff_controller.login(staff_id, password)
        
        if logged_in:
            staff = self.staff_controller.get_staff_by_id(staff_id)
            self.root.destroy()
            self.on_login_success(staff)
        else:
            staff = self.staff_controller.get_staff_by_id(staff_id)
            if staff and staff.getStatus() != "active":
                messagebox.showerror("Login Failed", 
                                   f"Account is {staff.getStatus()}.")
            else:
                messagebox.showerror("Login Failed", 
                                   "Invalid Staff ID or Password")
            self.password_var.set("")