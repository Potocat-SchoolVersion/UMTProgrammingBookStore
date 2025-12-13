# model/book_repository.py
import csv
import os
from model.book import Book
#Abstract Base Classes, import components from this module
from abc import ABC, abstractmethod
from tools.file_handler import read_file, save_file


class bookStorage(ABC):
    """Interface for book data operations"""
    @abstractmethod
    def load_books(self): pass
    
    @abstractmethod
    def save_books(self): pass
    
    @abstractmethod
    def get_book_by_id(self, book_id): pass
    
    @abstractmethod
    def update_stock(self, book_id, quantity): pass
    
    @abstractmethod
    def get_all_books(self): pass
    
    @abstractmethod
    def get_books_by_field(self, field): pass


class CSVBookRepository(bookStorage):    
    def __init__(self, csv_file='books.csv'):
        self.csv_file = csv_file
        self.books = []
        self.load_books()
    
    def load_books(self):
        """Load books"""
        self.books = []
        _file, ext = self.csv_file.split('.')
        reader = read_file(_file, ext)
        for row in reader:
            book = Book(
                row['bookID'],
                row['field'],
                row['bookName'],
                row['price'],
                row['stock'],
                row['sold']
            )
            self.books.append(book)
        return self.books
    
    def save_books(self):
        """Save books"""
        fieldnames = ['bookID', 'field', 'bookName', 'price', 'stock', 'sold']
        _file, ext = self.csv_file.split('.')
        save_file(_file, ext, fieldnames, self.books)
        # with open(self.csv_file, 'w', newline='') as file:
        #     fieldnames = ['bookID', 'field', 'bookName', 'price', 'stock', 'sold']
        #     writer = csv.DictWriter(file, fieldnames=fieldnames)
        #     writer.writeheader()
        #     for book in self.books:
        #         writer.writerow(book.to_dict())
    
    def get_book_by_id(self, book_id):
        """Get book by ID"""
        for book in self.books:
            if book.book_id.upper() == book_id.upper():
                return book
        return None
    
    def update_stock(self, book_id, quantity):
        """Update stock & sold count"""
        book = self.get_book_by_id(book_id)
        if book and book.has_sufficient_stock(quantity):
            book.update_stock(quantity)
            self.save_books()
            return True
        return False
    
    def get_all_books(self):
        """Get all books"""
        return self.books
    
    def get_books_by_field(self, field):
        """Get books by category"""
        return [book for book in self.books if book.field == field]
    
    def get_all_fields(self):
        """Get all unique fields, remove duplicate """
        return list(set(book.field for book in self.books))

