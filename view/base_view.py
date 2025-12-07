from tkinter import ttk
from abc import ABC, abstractmethod

class BaseView(ttk.Frame):
    """same frames for all"""
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.setup_ui()
    
    @abstractmethod
    def setup_ui(self):
        pass