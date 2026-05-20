import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import books
from books import BookCollection


@pytest.fixture(autouse=True)
def use_temp_data_file(tmp_path, monkeypatch):
    """Use a temporary data file for each test."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))


def test_add_book():
    collection = BookCollection()
    initial_count = len(collection.books)
    collection.add_book("1984", "George Orwell", 1949)
    assert len(collection.books) == initial_count + 1
    book = collection.find_book_by_title("1984")
    assert book is not None
    assert book.author == "George Orwell"
    assert book.year == 1949
    assert book.read is False


def test_mark_book_as_read():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    result = collection.mark_as_read("Dune")
    assert result is True
    book = collection.find_book_by_title("Dune")
    assert book.read is True


def test_mark_book_as_read_invalid():
    collection = BookCollection()
    result = collection.mark_as_read("Nonexistent Book")
    assert result is False


def test_remove_book_exact_and_returned_book():
    collection = BookCollection()
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    removed = collection.remove_book("The Hobbit")
    # Now remove_book returns the removed Book instance
    assert removed is not None
    assert isinstance(removed, books.Book)
    assert removed.title == "The Hobbit"
    # The book should no longer be findable
    book = collection.find_book_by_title("The Hobbit")
    assert book is None


def test_remove_book_invalid_returns_none():
    collection = BookCollection()
    removed = collection.remove_book("Nonexistent Book")
    assert removed is None


def test_remove_book_case_insensitive():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    # Different casing should still match
    removed = collection.remove_book("dUnE")
    assert removed is not None
    assert removed.title == "Dune"


def test_partial_title_does_not_match():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("Dune Messiah", "Frank Herbert", 1969)
    # Removing "Dune" should remove the exact title only
    removed = collection.remove_book("Dune")
    assert removed is not None
    # The longer title should still exist
    book = collection.find_book_by_title("Dune Messiah")
    assert book is not None


def test_unicode_normalization():
    collection = BookCollection()
    # Add a composed form
    collection.add_book("Café", "Some Author", 2000)
    # Remove using decomposed form (e + combining acute)
    removed = collection.remove_book("Cafe\u0301")
    assert removed is not None
    assert removed.title == "Café"
