# =================================================
#  Name = Parth Singh
#  Roll no = 2501730144
#  Course = B.tech CSE (AI/ML)
#  Section = D
# **********LIBRARY INVENTORY MANAGER ****
# =================================================

import json
from pathlib import Path

# -------------------- Book Class -------------------- #
class Book:
    """Represents a book in the library"""

    def __init__(self, title, author, isbn, status="available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status

    def __str__(self):
        return f"{self.title} by {self.author} | ISBN: {self.isbn} | {self.status.upper()}"

    def to_dict(self):
        return vars(self)

    @classmethod
    def from_json(cls, data):
        return cls(
            data['title'],
            data['author'],
            data['isbn'],
            data.get('status', 'available')
        )

    def mark_issued(self):
        if self.status == "available":
            self.status = "issued"
            return True
        return False

    def mark_returned(self):
        if self.status == "issued":
            self.status = "available"
            return True
        return False


# -------------------- Library Class -------------------- #
class Library:
    """Handles book inventory and JSON storage"""

    def __init__(self, file="library_data.json"):
        self.file = Path(file)
        self.books = []
        self.load_data()

    def add_book(self, book):
        if any(b.isbn == book.isbn for b in self.books):
            print("Book with this ISBN already exists!")
            return False

        self.books.append(book)
        self.save_data()
        print("Book added successfully.")
        return True

    def search_title(self, title):
        return [b for b in self.books if title.lower() in b.title.lower()]

    def search_isbn(self, isbn):
        return next((b for b in self.books if b.isbn == isbn), None)

    def search_author(self, author):
        return [b for b in self.books if author.lower() in b.author.lower()]

    def save_data(self):
        with open(self.file, "w") as f:
            json.dump([b.to_dict() for b in self.books], f, indent=4)

    def load_data(self):
        if self.file.exists():
            with open(self.file) as f:
                self.books = [Book.from_json(x) for x in json.load(f)]
        else:
            self.books = []

    def get_statistics(self):
        total = len(self.books)
        available = sum(b.status == "available" for b in self.books)
        return {"total": total, "available": available, "issued": total - available}

    def display_all(self):
        if not self.books:
            print("No books available!")
            return
        print("\n===== LIBRARY BOOKS =====")
        for b in self.books:
            print("-", b)
        print("=========================")


# -------------------- User Interface Functions -------------------- #

def ui_menu():
    print("""
========== Library Inventory ==========
1. Add Book
2. Issue Book
3. Return Book
4. Show All Books
5. Search by Title
6. Search by ISBN
7. Search by Author
8. View Statistics
9. Exit
=======================================
""")

def take_input(prompt):
    return input(prompt).strip()


def ui_add_book(lib):
    title = take_input("Book title: ")
    author = take_input("Author: ")
    isbn = take_input("ISBN: ")
    lib.add_book(Book(title, author, isbn))


def ui_issue_book(lib):
    isbn = take_input("ISBN to issue: ")
    book = lib.search_isbn(isbn)
    if not book:
        print("Book not found!")
    elif book.mark_issued():
        lib.save_data()
        print("Book issued.")
    else:
        print("Already issued.")


def ui_return_book(lib):
    isbn = take_input("ISBN to return: ")
    book = lib.search_isbn(isbn)
    if not book:
        print("Book not found!")
    elif book.mark_returned():
        lib.save_data()
        print("Book returned.")
    else:
        print("Book already available.")


def ui_search_by_title(lib):
    title = take_input("Search title: ")
    results = lib.search_title(title)
    print("\n".join(str(b) for b in results) if results else "No results.")


def ui_search_by_isbn(lib):
    isbn = take_input("Search ISBN: ")
    book = lib.search_isbn(isbn)
    print(book if book else "Book not found.")


def ui_search_by_author(lib):
    author = take_input("Search author: ")
    results = lib.search_author(author)
    print("\n".join(str(b) for b in results) if results else "No results.")


def ui_view_stats(lib):
    s = lib.get_statistics()
    print(f"Total: {s['total']} | Available: {s['available']} | Issued: {s['issued']}")


# -------------------- Main Program -------------------- #

def run_app():
    lib = Library()

    actions = {
        "1": ui_add_book,
        "2": ui_issue_book,
        "3": ui_return_book,
        "4": lambda l: l.display_all(),
        "5": ui_search_by_title,
        "6": ui_search_by_isbn,
        "7": ui_search_by_author,
        "8": ui_view_stats
    }

    while True:
        ui_menu()
        choice = take_input("Enter choice: ")

        if choice == "9":
            print("Goodbye!")
            break
        elif choice in actions:
            actions[choice](lib)
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    run_app()
