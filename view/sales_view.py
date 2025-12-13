import tkinter as tk
from tkinter import ttk, scrolledtext
from view.base_view import BaseView

class SalesView(BaseView):    
    def __init__(self, parent, sales_controller):
        self.sales_controller = sales_controller
        super().__init__(parent, sales_controller)
    
    def setup_ui(self):
        title = ttk.Label(self, text="📊 Sales Analytics", font=('Arial', 16, 'bold'))
        title.pack(pady=10)
        
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Button(btn_frame, text="📈 Sales Summary", 
                  command=self.show_sales_summary).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🏆 Top Sellers", 
                  command=self.show_top_sellers).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="💰 Revenue Analysis", 
                  command=self.show_revenue).pack(side='left', padx=5)

        ttk.Button(btn_frame, text="⚠️ Low Stock", 
                  command=self.show_low_stock).pack(side='left', padx=5)
        
        #Display area
        self.text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=80, 
                                               height=20, font=('Courier', 10))
        self.text_area.pack(fill='both', expand=True, padx=20, pady=10)
    
        #for color
        self.text_area.tag_config("warning", foreground="red", font=("Courier", 10, "bold"))
        self.text_area.tag_config("success", foreground="green", font=("Courier", 10, "bold"))    
        self.text_area.config(state='normal')


    #clean area before start design
    def clear_display(self):
        self.text_area.delete(1.0, tk.END)
    
    def show_sales_summary(self):
        self.text_area.config(state='normal')
        self.clear_display()
        summary = self.sales_controller.get_sales_summary()
        
        text = "="*114 + "\n"
        text += "\t\t\t\t\t"+ "SALES SUMMARY REPORT\n"
        text += "="*114 + "\n"
        text += f"{'Book ID':<10} {'Book Name':<35}\t\t\t\t\t {'Sold':>8}\t\t\t {'Revenue':>12}\n"
        text += "-"*114 
        
        for book in summary['books']:
            if book.sold > 0:
                text += f"{book.book_id:<10} {book.book_name:<35}\t\t\t\t\t {book.sold:>8} \t\tRM{book.calculate_revenue():>10.2f}\n"
        
        text += "-"*114 + "\n"
        text += f"{'TOTAL':<45} \t\t\t\t\t {summary['total_sold']:>8} \t\tRM{summary['total_revenue']:>10.2f}\n"
        text += "="*114 + "\n"
        
        self.text_area.insert(1.0, text)
        self.text_area.config(state='disabled')

    
    #most book
    def show_top_sellers(self):
        self.text_area.config(state='normal')
        self.clear_display()
        top_books = self.sales_controller.get_top_sellers(5)
        
        text = "="*114 + "\n"
        text += "\t\t\t\t\t"+ "TOP 5 SELLING BOOKS\n"
        text += "="*114  + "\n"
        text += f"{'Rank':<8} {'Book Name':<45} \t\t{'Units Sold':>12}\n"
        text += "-"*114
        
        for i, book in enumerate(top_books, 1):
            if book.sold > 0:
                text += f"{i:<8} {book.book_name:<45} \t\t{book.sold:>12}\n"
        
        text += "="*114 + "\n"
        self.text_area.insert(1.0, text)
        self.text_area.config(state='disabled')

    
    #profit by each book
    def show_revenue(self):        
        self.text_area.config(state='normal')
        self.clear_display() 
        revenue_books = self.sales_controller.get_highest_revenue(5)
        
        text = "="*114 + "\n"
        text += "\t\t\t\t\t"+ "TOP 5 REVENUE BOOKS\n"
        text += "="*114 + "\n"
        text += f"{'Rank':<8} {'Book Name':<45} \t\t\t {'Revenue':>12}\n"
        text += "-"*114
        
        for i, (book, revenue) in enumerate(revenue_books, 1):
            if revenue > 0:
                text += f"{i:<8} {book.book_name:<45} \t\t RM{revenue:>10.2f}\n"
        
        text += "="*114 + "\n"
        self.text_area.insert(1.0, text)
        self.text_area.config(state='disabled')

    

    
    def show_low_stock(self):
        self.text_area.config(state='normal')
        self.clear_display()
        low_stock = self.sales_controller.get_low_stock_books(20)

        # Insert header
        text = "="*114 + "\n"
        text += "\t\t\t\t\t"+ "⚠️  LOW STOCK ALERT (< 20 units)\n"
        text += "="*114 + "\n"
        self.text_area.insert(1.0, text)
    
        if low_stock:
            self.text_area.insert("end", f"{'Book ID':<10} {'Book Name':<45} \t\t{'Stock':>10}\n", "header")
            self.text_area.insert("end", "-" * 114 + "\n", "normal")
            
            for book in low_stock:
                text = f"{book.book_id:<10} {book.book_name:<45} {book.stock:>10}\n"
                self.text_area.insert("end", text, 'warning')

        else:
            self.text_area.insert("end", "\t\t\t\t\t"+"✅ All books have sufficient stock!\n", "success")
        
        self.text_area.insert("end", "=" * 114 + "\n", "header")
        self.text_area.config(state='disabled')
