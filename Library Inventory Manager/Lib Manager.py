# =================================================
# * Name = Parth Singh
# * Roll no = 2501730144
# * Course = B.tech CSE (AI/ML)
# * Section = D
# **********LIBRARY INVENTORY MANAGER ************
# =================================================

class Book:
    """Class representing a book in the library"""
    
    def __init__(self, title, author, isbn, status="available"):
        """
        Initialize a Book object
        
        Args:
            title (str): Book title
            author (str): Book author
            isbn (str): ISBN number
            status (str): Book status (available/issued)
        """
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status
    
    def __str__(self):
        """String representation of the book"""
        return f"'{self.title}' by {self.author} [ISBN: {self.isbn}] - {self.status.upper()}"
    
    def to_dict(self):
        """Convert book to dictionary for JSON serialization"""
        return {
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'status': self.status
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create Book object from dictionary"""
        return cls(
            data['title'],
            data['author'],
            data['isbn'],
            data.get('status', 'available')
        )
    
    def issue(self):
        """Issue the book"""
        if self.status == "available":
            self.status = "issued"
            return True
        return False
    
    def return_book(self):
        """Return the book to library"""
        if self.status == "issued":
            self.status = "available"
            return True
        return False
    
    def is_available(self):
        """Check if book is available"""
        return self.status == "available"
"""
Library Inventory Manager
Manages collection of books with file persistence
"""
import json
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('library.log'),
        logging.StreamHandler()
    ]
)

class LibraryInventory:
    """Manages library book inventory"""
    
    def __init__(self, data_file="library_data.json"):
        """
        Initialize Library Inventory
        
        Args:
            data_file (str): Path to JSON data file
        """
        self.data_file = Path(data_file)
        self.books = []
        self.load_data()
        logging.info("Library Inventory initialized")
    
    def add_book(self, book):
        """
        Add a book to inventory
        
        Args:
            book (Book): Book object to add
        """
        try:
            # Check for duplicate ISBN
            if any(b.isbn == book.isbn for b in self.books):
                logging.warning(f"Book with ISBN {book.isbn} already exists")
                return False
            
            self.books.append(book)
            self.save_data()
            logging.info(f"Added book: {book.title}")
            return True
        except Exception as e:
            logging.error(f"Error adding book: {e}")
            return False
    
    def search_by_title(self, title):
        """Search books by title (case-insensitive, partial match)"""
        results = [b for b in self.books if title.lower() in b.title.lower()]
        logging.info(f"Search by title '{title}': {len(results)} results")
        return results
    
    def search_by_isbn(self, isbn):
        """Search book by ISBN"""
        for book in self.books:
            if book.isbn == isbn:
                logging.info(f"Found book with ISBN {isbn}")
                return book
        logging.info(f"No book found with ISBN {isbn}")
        return None
    
    def search_by_author(self, author):
        """Search books by author (case-insensitive, partial match)"""
        results = [b for b in self.books if author.lower() in b.author.lower()]
        logging.info(f"Search by author '{author}': {len(results)} results")
        return results
    
    def display_all(self):
        """Display all books in inventory"""
        if not self.books:
            print("\\nNo books in inventory.")
            return
        
        print(f"\\n{'='*80}")
        print(f"{'LIBRARY INVENTORY':^80}")
        print(f"{'='*80}")
        print(f"{'#':<5} {'Title':<30} {'Author':<25} {'ISBN':<15} {'Status':<10}")
        print(f"{'-'*80}")
        
        for idx, book in enumerate(self.books, 1):
            print(f"{idx:<5} {book.title[:28]:<30} {book.author[:23]:<25} "
                  f"{book.isbn:<15} {book.status.upper():<10}")
        
        print(f"{'='*80}")
        print(f"Total Books: {len(self.books)}")
        print()
    
    def save_data(self):
        """Save inventory to JSON file"""
        try:
            data = [book.to_dict() for book in self.books]
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            logging.info(f"Data saved to {self.data_file}")
        except IOError as e:
            logging.error(f"Failed to save data: {e}")
        except Exception as e:
            logging.error(f"Unexpected error saving data: {e}")
    
    def load_data(self):
        """Load inventory from JSON file"""
        try:
            if self.data_file.exists():
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.books = [Book.from_dict(item) for item in data]
                logging.info(f"Loaded {len(self.books)} books from {self.data_file}")
            else:
                logging.info(f"Data file {self.data_file} not found. Starting fresh.")
                self.books = []
        except json.JSONDecodeError as e:
            logging.error(f"Corrupted JSON file: {e}. Starting with empty inventory.")
            self.books = []
        except Exception as e:
            logging.error(f"Error loading data: {e}")
            self.books = []
    
    def get_statistics(self):
        """Get inventory statistics"""
        total = len(self.books)
        available = sum(1 for b in self.books if b.is_available())
        issued = total - available
        return {'total': total, 'available': available, 'issued': issued}
    
"""
Command Line Interface for Library Inventory Manager
Main entry point for the application
"""

import logging
# from inventory import LibraryInventory
# from book import Book

def print_menu():
    """Display main menu"""
    print("\\n" + "="*50)
    print("  LIBRARY INVENTORY MANAGEMENT SYSTEM")
    print("="*50)
    print("1. Add New Book")
    print("2. Issue Book")
    print("3. Return Book")
    print("4. View All Books")
    print("5. Search by Title")
    print("6. Search by ISBN")
    print("7. Search by Author")
    print("8. View Statistics")
    print("9. Exit")
    print("="*50)

def get_input(prompt, input_type=str, allow_empty=False):
    """
    Get validated user input
    
    Args:
        prompt (str): Input prompt
        input_type (type): Expected input type
        allow_empty (bool): Allow empty input
    """
    while True:
        try:
            value = input(prompt).strip()
            if not value and not allow_empty:
                print("Input cannot be empty. Please try again.")
                continue
            if input_type == int:
                return int(value)
            return value
        except ValueError:
            print(f"Invalid input. Expected {input_type.__name__}.")
        except KeyboardInterrupt:
            print("\\nOperation cancelled.")
            return None

def add_book_menu(inventory):
    """Add book menu handler"""
    print("\\n--- Add New Book ---")
    title = get_input("Enter book title: ")
    if not title:
        return
    
    author = get_input("Enter author name: ")
    if not author:
        return
    
    isbn = get_input("Enter ISBN: ")
    if not isbn:
        return
    
    book = Book(title, author, isbn)
    if inventory.add_book(book):
        print(f"\\n✓ Book added successfully: {book}")
    else:
        print(f"\\n✗ Failed to add book. ISBN may already exist.")

def issue_book_menu(inventory):
    """Issue book menu handler"""
    print("\\n--- Issue Book ---")
    isbn = get_input("Enter ISBN of book to issue: ")
    if not isbn:
        return
    
    book = inventory.search_by_isbn(isbn)
    if not book:
        print(f"\\n✗ No book found with ISBN: {isbn}")
        return
    
    if book.issue():
        inventory.save_data()
        print(f"\\n✓ Book issued successfully: {book}")
    else:
        print(f"\\n✗ Book is already issued: {book}")

def return_book_menu(inventory):
    """Return book menu handler"""
    print("\\n--- Return Book ---")
    isbn = get_input("Enter ISBN of book to return: ")
    if not isbn:
        return
    
    book = inventory.search_by_isbn(isbn)
    if not book:
        print(f"\\n✗ No book found with ISBN: {isbn}")
        return
    
    if book.return_book():
        inventory.save_data()
        print(f"\\n✓ Book returned successfully: {book}")
    else:
        print(f"\\n✗ Book is already available: {book}")

def search_title_menu(inventory):
    """Search by title menu handler"""
    print("\\n--- Search by Title ---")
    title = get_input("Enter title to search: ")
    if not title:
        return
    
    results = inventory.search_by_title(title)
    if results:
        print(f"\\nFound {len(results)} book(s):")
        for idx, book in enumerate(results, 1):
            print(f"{idx}. {book}")
    else:
        print(f"\\n✗ No books found with title containing: {title}")

def search_isbn_menu(inventory):
    """Search by ISBN menu handler"""
    print("\\n--- Search by ISBN ---")
    isbn = get_input("Enter ISBN to search: ")
    if not isbn:
        return
    
    book = inventory.search_by_isbn(isbn)
    if book:
        print(f"\\nFound: {book}")
    else:
        print(f"\\n✗ No book found with ISBN: {isbn}")

def search_author_menu(inventory):
    """Search by author menu handler"""
    print("\\n--- Search by Author ---")
    author = get_input("Enter author name to search: ")
    if not author:
        return
    
    results = inventory.search_by_author(author)
    if results:
        print(f"\\nFound {len(results)} book(s):")
        for idx, book in enumerate(results, 1):
            print(f"{idx}. {book}")
    else:
        print(f"\\n✗ No books found by author: {author}")

def view_statistics(inventory):
    """Display inventory statistics"""
    stats = inventory.get_statistics()
    print("\\n" + "="*50)
    print("  INVENTORY STATISTICS")
    print("="*50)
    print(f"Total Books:     {stats['total']}")
    print(f"Available:       {stats['available']}")
    print(f"Issued:          {stats['issued']}")
    print("="*50)

def main():
    """Main application loop"""
    print("\\n🏛️  Welcome to Library Inventory Manager")
    print("Loading inventory...")
    
    try:
        inventory = LibraryInventory()
        
        menu_options = {
            '1': add_book_menu,
            '2': issue_book_menu,
            '3': return_book_menu,
            '4': lambda inv: inv.display_all(),
            '5': search_title_menu,
            '6': search_isbn_menu,
            '7': search_author_menu,
            '8': view_statistics,
        }
        
        while True:
            try:
                print_menu()
                choice = get_input("Enter your choice (1-9): ")
                
                if choice == '9':
                    print("\\n Thank you for using Library Inventory Manager!")
                    logging.info("Application closed by user")
                    break
                
                if choice in menu_options:
                    menu_options[choice](inventory)
                else:
                    print("\\n✗ Invalid choice. Please enter a number between 1-9.")
            
            except KeyboardInterrupt:
                print("\\n\\n Application interrupted. Goodbye!")
                break
            except Exception as e:
                logging.error(f"Unexpected error in main loop: {e}")
                print(f"\\n✗ An error occurred: {e}")
    
    except Exception as e:
        logging.critical(f"Failed to initialize application: {e}")
        print(f"\\n✗ Critical error: {e}")

if __name__ == "__main__":

    main()
