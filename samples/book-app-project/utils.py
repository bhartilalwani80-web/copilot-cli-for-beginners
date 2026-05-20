def display_menu():
    print("\n📚 Book Collection App")
    print("1. Add a book")
    print("2. List books")
    print("3. Mark book as read")
    print("4. Remove a book")
    print("5. Exit")


def get_user_choice() -> str:
    return input("Choose an option (1-5): ").strip()


def get_book_details():
    """Prompt the user for book details and return (title, author, year, warnings).

    Warnings is a list of strings representing non-fatal issues (e.g. 'invalid_year').
    This function performs input reading and parsing but does not print warnings itself.
    """
    title = input("Enter book title: ").strip()
    author = input("Enter author: ").strip()

    year_input = input("Enter publication year: ").strip()
    warnings = []
    try:
        year = int(year_input) if year_input else 0
    except ValueError:
        year = 0
        warnings.append("invalid_year")

    return title, author, year, warnings


def show_books(books):
    if not books:
        print("No books in your collection.")
        return

    print("\nYour Books:")
    for index, book in enumerate(books, start=1):
        status = "✅ Read" if getattr(book, "read", False) else "📖 Unread"
        title = getattr(book, "title", "<unknown>")
        author = getattr(book, "author", "<unknown>")
        year = getattr(book, "year", "?")
        print(f"{index}. {title} by {author} ({year}) - {status}")


# Display helpers
def display_message(msg: str):
    print(msg)


def display_error(msg: str):
    print(f"Error: {msg}")


# Backwards compatibility
print_books = show_books
