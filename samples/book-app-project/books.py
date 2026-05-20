import json
import unicodedata
from dataclasses import dataclass, asdict
from typing import List, Optional

DATA_FILE = "data.json"


@dataclass
class Book:
    title: str
    author: str
    year: int
    read: bool = False


class BookCollection:
    def __init__(self):
        self.books: List[Book] = []
        self.load_books()

    def load_books(self):
        """Load books from the JSON file if it exists."""
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                self.books = [Book(**b) for b in data]
        except FileNotFoundError:
            self.books = []
        except json.JSONDecodeError:
            print("Warning: data.json is corrupted. Starting with empty collection.")
            self.books = []

    def save_books(self):
        """Save the current book collection to JSON."""
        with open(DATA_FILE, "w") as f:
            json.dump([asdict(b) for b in self.books], f, indent=2)

    def add_book(self, title: str, author: str, year: int) -> Book:
        book = Book(title=title, author=author, year=year)
        self.books.append(book)
        self.save_books()
        return book

    def list_books(self) -> List[Book]:
        return self.books

    def _normalize(self, s: str) -> str:
        """Normalize strings for comparisons (NFC, strip, casefold)."""
        if s is None:
            return ""
        return unicodedata.normalize("NFC", s).strip().casefold()

    def find_book_by_title(self, title: str) -> Optional[Book]:
        query = self._normalize(title)
        if not query:
            return None
        for book in self.books:
            if self._normalize(book.title) == query:
                return book
        return None

    def mark_as_read(self, title: str) -> bool:
        book = self.find_book_by_title(title)
        if book:
            book.read = True
            self.save_books()
            return True
        return False

    def remove_book(self, title: str) -> Optional[Book]:
        """Remove a book by title (case-insensitive).

        Returns the removed Book if successful, or None if no match was found.
        """
        book = self.find_book_by_title(title)
        if book:
            # remove from in-memory list first
            self.books.remove(book)
            try:
                self.save_books()
            except Exception:
                # on failure, restore the book to keep in-memory state consistent
                self.books.append(book)
                raise
            return book
        return None

    def find_by_author(self, author: str) -> List[Book]:
        """Find all books by a given author (case-insensitive, supports partial matches)."""
        query = author.strip().lower()
        if not query:
            return []
        return [b for b in self.books if query in b.author.lower()]
