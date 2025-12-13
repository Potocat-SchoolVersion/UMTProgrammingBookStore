# view/order_view.py
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import cv2

from view.base_view import BaseView
from model.discount import Discount


class OrderView(BaseView):
    """View for creating orders (UI-focused; logic delegated to controller)."""

    def __init__(self, parent, order_controller, on_order_complete):
        self.order_controller = order_controller
        self.on_order_complete = on_order_complete

        # map book_id -> treeview item iid (to support merged rows)
        self._cart_row_iids = {}

        super().__init__(parent, order_controller)

    def setup_ui(self):
        # Title
        title = ttk.Label(self, text="🛒 Create Sales Order", font=('Arial', 16, 'bold'))
        title.pack(pady=10)

        # ------------------------
        # Input frame
        # ------------------------
        input_frame = ttk.LabelFrame(self, text="Add Items to Cart", padding=10)
        input_frame.pack(fill='x', padx=20, pady=10)

        ttk.Label(input_frame, text="Book ID:").grid(row=0, column=0, sticky='w', padx=5, pady=5)

        self.book_id_var = tk.StringVar()
        self.book_id_cb = ttk.Combobox(
            input_frame,
            textvariable=self.book_id_var,
            width=15,
            state="readonly",
            values=[]
        )
        self.book_id_cb.grid(row=0, column=1, padx=5, pady=5)
        self.book_id_cb.bind("<<ComboboxSelected>>", lambda e: self.on_book_selected())

        ttk.Button(input_frame, text="📷 Scan QR", command=self.scan_qr).grid(row=0, column=2, padx=5, pady=5)

        self.book_name_label = ttk.Label(input_frame, text="", foreground="blue")
        self.book_name_label.grid(row=1, column=0, columnspan=3, sticky='w', padx=5, pady=2)

        ttk.Label(input_frame, text="Quantity:").grid(row=2, column=0, sticky='w', padx=5, pady=5)

        self.quantity_var = tk.StringVar(value="1")
        self.quantity_spin = ttk.Spinbox(
            input_frame,
            from_=1,
            to=1,
            textvariable=self.quantity_var,
            width=15,
            state="disabled"
        )
        self.quantity_spin.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(input_frame, text="➕ Add to Cart", command=self.add_to_cart).grid(row=2, column=2, padx=5, pady=5)

        # ------------------------
        # Cart frame (tree only)
        # ------------------------
        cart_frame = ttk.LabelFrame(self, text="Shopping Cart", padding=10)
        cart_frame.pack(fill='both', expand=True, padx=20, pady=10)

        columns = ('ID', 'Name', 'Price', 'Qty', 'Total')
        self.cart_tree = ttk.Treeview(cart_frame, columns=columns, show='headings', height=8)

        self.cart_tree.heading('ID', text='Book ID')
        self.cart_tree.heading('Name', text='Book Name')
        self.cart_tree.heading('Price', text='Price')
        self.cart_tree.heading('Qty', text='Qty')
        self.cart_tree.heading('Total', text='Total')

        self.cart_tree.column('ID', width=80)
        self.cart_tree.column('Name', width=300)
        self.cart_tree.column('Price', width=100)
        self.cart_tree.column('Qty', width=80)
        self.cart_tree.column('Total', width=100)

        self.cart_tree.pack(side='left', fill='both', expand=True)

        cart_scrollbar = ttk.Scrollbar(cart_frame, orient='vertical', command=self.cart_tree.yview)
        self.cart_tree.configure(yscrollcommand=cart_scrollbar.set)
        cart_scrollbar.pack(side='right', fill='y')

        # ------------------------
        # Checkout frame (form)
        # ------------------------
        checkout_frame = ttk.LabelFrame(self, text="Checkout", padding=10)
        checkout_frame.pack(fill='x', padx=20, pady=10)

        # Vars
        self.subtotal_var = tk.StringVar(value="0.00")
        self.voucher_var = tk.StringVar(value="")
        self.voucher_text_var = tk.StringVar(value="")   # display get_discount_text(voucher)
        self.discount_var = tk.StringVar(value="0.00")
        self.tax_var = tk.StringVar(value="0.00")
        self.total_var = tk.StringVar(value="0.00")
        self.cash_received_var = tk.StringVar(value="")
        self.balance_var = tk.StringVar(value="0.00")

        # Row 0: Subtotal (readonly)
        ttk.Label(checkout_frame, text="Subtotal (RM):").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        ttk.Entry(checkout_frame, textvariable=self.subtotal_var, state="readonly", width=20).grid(row=0, column=1, padx=5, pady=5)

        # Row 1: Voucher + voucher text
        ttk.Label(checkout_frame, text="Discount Voucher:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.voucher_entry = ttk.Entry(checkout_frame, textvariable=self.voucher_var, width=20)
        self.voucher_entry.grid(row=1, column=1, padx=5, pady=5)

        self.voucher_text_label = ttk.Label(checkout_frame, textvariable=self.voucher_text_var, foreground="gray")
        self.voucher_text_label.grid(row=1, column=2, sticky='w', padx=5, pady=5)

        # Row 2: Discount (readonly)
        ttk.Label(checkout_frame, text="Discount (RM):").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        ttk.Entry(checkout_frame, textvariable=self.discount_var, state="readonly", width=20).grid(row=2, column=1, padx=5, pady=5)

        # Row 3: Tax (readonly)
        ttk.Label(checkout_frame, text="Tax (RM):").grid(row=3, column=0, sticky='w', padx=5, pady=5)
        ttk.Entry(checkout_frame, textvariable=self.tax_var, state="readonly", width=20).grid(row=3, column=1, padx=5, pady=5)

        # Row 4: Total (readonly)
        ttk.Label(checkout_frame, text="Total (RM):").grid(row=4, column=0, sticky='w', padx=5, pady=5)
        ttk.Entry(checkout_frame, textvariable=self.total_var, state="readonly", width=20).grid(row=4, column=1, padx=5, pady=5)

        # Row 5: Cash Received (user input)
        ttk.Label(checkout_frame, text="Cash Received (RM):").grid(row=5, column=0, sticky='w', padx=5, pady=5)
        ttk.Entry(checkout_frame, textvariable=self.cash_received_var, width=20).grid(row=5, column=1, padx=5, pady=5)

        # Row 6: Balance (readonly)
        ttk.Label(checkout_frame, text="Balance (RM):").grid(row=6, column=0, sticky='w', padx=5, pady=5)
        ttk.Entry(checkout_frame, textvariable=self.balance_var, state="readonly", width=20).grid(row=6, column=1, padx=5, pady=5)

        # Buttons row
        btn_row = ttk.Frame(checkout_frame)
        btn_row.grid(row=7, column=0, columnspan=3, sticky='e', padx=5, pady=10)

        ttk.Button(btn_row, text="🧮 Calculate", command=self.calculate_checkout).pack(side='left', padx=5)
        ttk.Button(btn_row, text="✅ Process Order", command=self.process_order).pack(side='left', padx=5)

        # Clear cart button stays below
        bottom_btn_frame = ttk.Frame(self)
        bottom_btn_frame.pack(fill='x', padx=20, pady=(0, 10))
        ttk.Button(bottom_btn_frame, text="🗑️ Clear Cart", command=self.clear_cart).pack(side='left', padx=5)

        # Initialize UI state
        self.start_new_order()
        self.refresh_book_dropdown()
        self.update_subtotal_only()

    # ------------------------
    # Availability helpers
    # ------------------------

    def refresh_book_dropdown(self):
        """Populate Book ID dropdown with only books that have (stock - reserved_in_cart) > 0."""
        repo = self.order_controller.repository
        available_ids = []

        for book in repo.get_all_books():
            if self.get_available_stock(book.book_id) > 0:
                available_ids.append(book.book_id)

        available_ids.sort()
        current = self.book_id_var.get().strip()
        self.book_id_cb["values"] = available_ids

        # If current selection is no longer valid, clear it
        if current and current not in available_ids:
            self._clear_book_selection_ui()

    def get_reserved_qty(self, book_id: str) -> int:
        """How many units of this book are already in the cart?"""
        for item in self.order_controller.order_item_list:
            if item.book_id.upper() == book_id.upper():
                return int(item.quantity)
        return 0

    def get_available_stock(self, book_id: str) -> int:
        """available = current stock - reserved in cart"""
        book = self.order_controller.repository.get_book_by_id(book_id)
        if not book:
            return 0
        return int(book.stock) - self.get_reserved_qty(book_id)

    def on_book_selected(self):
        """When a book is selected: show name and update Spinbox max based on available stock."""
        book_id = self.book_id_var.get().strip()
        if not book_id:
            self._clear_book_selection_ui()
            return

        book = self.order_controller.repository.get_book_by_id(book_id)
        if not book:
            self.book_name_label.config(text="❌ Book not found", foreground="red")
            self.quantity_spin.config(state="disabled", from_=1, to=1)
            self.quantity_var.set("1")
            return

        self.book_name_label.config(text=f"📚 {book.book_name}", foreground="green")

        available = self.get_available_stock(book_id)
        if available <= 0:
            self.quantity_spin.config(state="disabled", from_=1, to=1)
            self.quantity_var.set("1")
        else:
            self.quantity_spin.config(state="normal", from_=1, to=available)
            self.quantity_var.set("1")

    def scan_qr(self):
        """Dummy QR scan hook."""
        messagebox.showinfo("Scan QR", "QR scanning not implemented yet.")

    def _clear_book_selection_ui(self):
        self.book_id_var.set("")
        self.book_name_label.config(text="", foreground="blue")
        self.quantity_spin.config(state="disabled", from_=1, to=1)
        self.quantity_var.set("1")

    # ------------------------
    # Cart / Order UI actions
    # ------------------------

    def start_new_order(self):
        """Reset the view + controller cart state."""
        self.order_controller.order_item_list = []
        self._cart_row_iids = {}
        self._clear_book_selection_ui()

        # reset checkout fields (except subtotal which will be updated)
        self.voucher_var.set("")
        self.voucher_text_var.set("")
        self.discount_var.set("0.00")
        self.tax_var.set("0.00")
        self.total_var.set("0.00")
        self.cash_received_var.set("")
        self.balance_var.set("0.00")

    def add_to_cart(self):
        """Add selected book + quantity to cart (merged rows)."""
        book_id = self.book_id_var.get().strip()
        if not book_id:
            messagebox.showerror("Error", "Please select a Book ID.")
            return

        try:
            quantity = int(self.quantity_var.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity!")
            return

        if quantity <= 0:
            messagebox.showerror("Error", "Quantity must be greater than 0.")
            return

        # Validate book
        book = self.order_controller.repository.get_book_by_id(book_id)
        if not book:
            messagebox.showerror("Error", "Book not found!")
            return

        # Validate against available stock (UI should prevent it, but keep guard anyway)
        available = self.get_available_stock(book_id)
        if quantity > available:
            messagebox.showerror("Error", f"Insufficient stock available.\nAvailable: {available}")
            return

        # Delegate to controller (merge logic lives there)
        self.order_controller.add_item_to_order(book, quantity)

        # Find merged item from controller list
        merged_item = None
        for it in self.order_controller.order_item_list:
            if it.book_id.upper() == book_id.upper():
                merged_item = it
                break

        if merged_item is None:
            messagebox.showerror("Error", "Failed to add item to cart.")
            return

        # Update Treeview (insert or update existing row)
        price_text = f"RM{float(book.price):.2f}"
        total_text = f"RM{float(merged_item.line_total):.2f}"

        if book_id in self._cart_row_iids:
            iid = self._cart_row_iids[book_id]
            self.cart_tree.item(iid, values=(book_id, book.book_name, price_text, merged_item.quantity, total_text))
        else:
            iid = self.cart_tree.insert('', 'end', values=(book_id, book.book_name, price_text, merged_item.quantity, total_text))
            self._cart_row_iids[book_id] = iid

        # Refresh availability UI + subtotal only
        self.refresh_book_dropdown()
        self.on_book_selected()  # updates spinbox max for currently selected book
        self.update_subtotal_only()

    def update_subtotal_only(self):
        """Auto-update subtotal whenever cart changes (no other calculations)."""
        subtotal = 0.0
        for item in self.order_controller.order_item_list:
            subtotal += float(item.line_total)

        self.subtotal_var.set(f"{subtotal:.2f}")

        # Since subtotal changed, old calculated values are stale -> reset calculated fields
        self.discount_var.set("0.00")
        self.tax_var.set("0.00")
        self.total_var.set("0.00")
        self.balance_var.set("0.00")
        self.voucher_text_var.set("")

    def calculate_checkout(self):
        """
        Calculate discount/tax/total + balance.
        Only runs when user clicks Calculate.
        """
        if not self.order_controller.order_item_list:
            messagebox.showwarning("Warning", "Cart is empty!")
            return

        voucher = self.voucher_var.get().strip().upper()

        # Validate voucher and show text
        try:
            voucher_text = Discount.get_discount_text(voucher)
            discount_rate = Discount.get_discount_rate(voucher)
            self.voucher_text_var.set(voucher_text)
        except Exception:
            messagebox.showerror("Error", "Invalid voucher code.")
            self.voucher_text_var.set("")
            return

        # Subtotal (from cart)
        subtotal = sum(float(item.line_total) for item in self.order_controller.order_item_list)

        # Discount amount
        discount_amount = subtotal * float(discount_rate)
        after_discount = subtotal - discount_amount

        # Tax: use controller tax rate if available; else default 0.06
        tax_rate = 0.06
        if hasattr(self.order_controller, "get_tax_rate"):
            tax_rate = float(self.order_controller.get_tax_rate())

        tax_amount = after_discount * tax_rate
        total = after_discount + tax_amount

        # Cash received -> balance
        cash_str = self.cash_received_var.get().strip()
        if cash_str == "":
            cash = 0.0
        else:
            try:
                cash = float(cash_str)
            except ValueError:
                messagebox.showerror("Error", "Cash Received must be a number.")
                return

        balance = cash - total

        # Display
        self.subtotal_var.set(f"{subtotal:.2f}")
        self.discount_var.set(f"{discount_amount:.2f}")
        self.tax_var.set(f"{tax_amount:.2f}")
        self.total_var.set(f"{total:.2f}")
        self.balance_var.set(f"{balance:.2f}")

    def clear_cart(self):
        """Clear cart UI + controller state."""
        # Clear tree
        for iid in self.cart_tree.get_children():
            self.cart_tree.delete(iid)

        # Reset controller+view state
        self.start_new_order()
        self.refresh_book_dropdown()
        self.update_subtotal_only()

    def process_order(self):
        """
        Placeholder hook: commit logic later.
        """
        if not self.order_controller.order_item_list:
            messagebox.showwarning("Warning", "Cart is empty!")
            return

        if not messagebox.askyesno("Confirm Order", "Process this order?"):
            return

        messagebox.showinfo("Process Order", "commit_order() not implemented yet.")

    def start_new_order(self):
        """Reset the view + controller cart state."""
        if hasattr(self.order_controller, "reset_order"):
            self.order_controller.reset_order()
        else:
            self.order_controller.order_item_list = []

        self._cart_row_iids = {}
        self._clear_book_selection_ui()

        # reset checkout fields
        self.subtotal_var.set("0.00")
        self.voucher_var.set("")
        self.voucher_text_var.set("")
        self.discount_var.set("0.00")
        self.tax_var.set("0.00")
        self.total_var.set("0.00")
        self.cash_received_var.set("")
        self.balance_var.set("0.00")

    def process_order(self):
        """Commit order (controller handles persistence + stock update)."""
        if not self.order_controller.order_item_list:
            messagebox.showwarning("Warning", "Cart is empty!")
            return

        if not messagebox.askyesno("Confirm Order", "Process this order?"):
            return

        voucher = self.voucher_var.get().strip().upper()

        cash_str = self.cash_received_var.get().strip()
        if cash_str == "":
            messagebox.showerror("Error", "Please enter Cash Received.")
            return

        # Commit through controller
        ok, msg, receipt = self.order_controller.commit_order(voucher, cash_str)

        if not ok:
            messagebox.showerror("Error", msg)
            return

        # Show a simple receipt popup
        lines = []
        lines.append(f"Order ID: {receipt['order_id']}")
        lines.append(f"Date/Time: {receipt['date_time']}")
        lines.append(f"Staff ID: {receipt['staff_id']}")
        lines.append("=" * 40)
        for it in receipt["items"]:
            lines.append(f"{it['bookID']}  x{it['quantity']}  RM{it['price_at_sale']:.2f}  =  RM{it['line_total']:.2f}")
        lines.append("=" * 40)
        lines.append(f"Subtotal: RM{receipt['subtotal']:.2f}")
        lines.append(f"Voucher: {receipt['voucher'] or '-'} ({receipt['discount_text']})")
        lines.append(f"Discount: RM{receipt['discount']:.2f}")
        lines.append(f"Tax:      RM{receipt['tax']:.2f}")
        lines.append(f"TOTAL:    RM{receipt['total']:.2f}")
        lines.append(f"Cash:     RM{receipt['cash_received']:.2f}")
        lines.append(f"Balance:  RM{receipt['balance']:.2f}")

        messagebox.showinfo("Order Successful", "\n".join(lines))

        # Clear cart UI
        for iid in self.cart_tree.get_children():
            self.cart_tree.delete(iid)

        # Reset view state (controller already reset after commit)
        self._cart_row_iids = {}
        self.refresh_book_dropdown()
        self._clear_book_selection_ui()

        # Update totals fields to reflect empty cart
        self.subtotal_var.set("0.00")
        self.discount_var.set("0.00")
        self.tax_var.set("0.00")
        self.total_var.set("0.00")
        self.balance_var.set("0.00")
        self.voucher_text_var.set("")

        # Let main window refresh books tab
        self.on_order_complete()













    # ------------------------
    # QR Scan (OpenCV window)
    # ------------------------

    def scan_qr(self):
        """
        Start QR scanning in a background thread (so Tk doesn't freeze).
        Shows an OpenCV window. On success -> sets combobox selection.
        """
        # Prevent multiple scan sessions at once
        if getattr(self, "_scan_thread", None) and self._scan_thread.is_alive():
            messagebox.showinfo("Scan QR", "Already scanning...")
            return

        self._scan_cancel = False
        self._scan_thread = threading.Thread(target=self._scan_qr_worker, daemon=True)
        self._scan_thread.start()

    def _scan_qr_worker(self):
        """
        Worker thread: opens camera, shows cv2 window, detects QR code for up to 10 seconds.
        Does not touch Tk widgets directly -> schedules UI updates via self.after().
        """
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # CAP_DSHOW helps on some Windows setups
        if not cap.isOpened():
            self.after(0, lambda: messagebox.showerror("Camera Error", "Camera not available / permission denied."))
            return

        detector = cv2.QRCodeDetector()
        start = time.time()
        decoded_text = None

        try:
            while True:
                # Timeout
                if time.time() - start >= 10:
                    break

                # Allow cancel by ESC in OpenCV window
                ret, frame = cap.read()
                if not ret:
                    # if camera read fails, treat like camera error
                    self.after(0, lambda: messagebox.showerror("Camera Error", "Failed to read from camera."))
                    return

                # Detect + decode
                data, points, _ = detector.detectAndDecode(frame)

                # Draw bounding box if detected
                if points is not None and len(points) > 0:
                    pts = points.astype(int)
                    # pts shape is usually (1,4,2); normalize
                    if pts.ndim == 3:
                        pts = pts[0]
                    for i in range(len(pts)):
                        p1 = tuple(pts[i])
                        p2 = tuple(pts[(i + 1) % len(pts)])
                        cv2.line(frame, p1, p2, (0, 255, 0), 2)

                # Show window
                cv2.imshow("Scan QR (ESC to cancel)", frame)

                # Keyboard handling
                key = cv2.waitKey(1) & 0xFF
                if key == 27:  # ESC
                    self._scan_cancel = True
                    break

                # If decoded
                if data:
                    decoded_text = data.strip()
                    break

        finally:
            cap.release()
            try:
                cv2.destroyWindow("Scan QR (ESC to cancel)")
            except Exception:
                cv2.destroyAllWindows()

        # Handle outcomes
        if self._scan_cancel:
            self.after(0, lambda: messagebox.showinfo("Scan QR", "Scan cancelled."))
            return

        if not decoded_text:
            self.after(0, lambda: messagebox.showwarning("Scan QR", "No QR detected (timeout 10 seconds)."))
            return

        # Assume QR is plain bookID like "B001"
        book_id = decoded_text.upper()

        # Validate book exists
        book = self.order_controller.repository.get_book_by_id(book_id)
        if not book:
            self.after(0, lambda: messagebox.showerror("Scan QR", f"Book not found: {book_id}"))
            return

        # Validate availability (stock - reserved in cart)
        available = self.get_available_stock(book_id)
        if available <= 0:
            self.after(0, lambda: messagebox.showerror("Scan QR", f"Book {book_id} has no available stock."))
            return

        # Apply to UI in main thread
        self.after(0, lambda: self._apply_scanned_book(book_id))

    def _apply_scanned_book(self, book_id: str):
        """
        Apply scanned bookID into the combobox selection + update name/spinbox.
        Must run on Tk main thread.
        """
        # Ensure dropdown values are up-to-date
        self.refresh_book_dropdown()

        values = list(self.book_id_cb["values"])
        if book_id not in values:
            # This can happen if available became 0 due to cart reservation
            messagebox.showerror("Scan QR", f"Book {book_id} is not selectable (maybe no stock available).")
            return

        self.book_id_var.set(book_id)
        self.on_book_selected()
