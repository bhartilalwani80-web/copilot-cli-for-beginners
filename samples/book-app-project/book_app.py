import sys
from books import BookCollection


# Global collection instance
collection = BookCollection()


from utils import show_books, get_book_details, display_message, display_error

def handle_list():
    books = collection.list_books()
    show_books(books)


def handle_add():
    display_message("\nAdd a New Book\n")

    title, author, year, warnings = get_book_details()

    if not title or not author:
        display_error("Title and author are required.")
        return

    collection.add_book(title, author, year)

    if "invalid_year" in warnings:
        display_message("Invalid year input; defaulted to 0.")

    display_message("\nBook added successfully.\n")


def handle_remove():
    display_message("\nRemove a Book\n")

    title = input("Enter the title of the book to remove: ").strip()
    if not title:
        display_error("Title is required.")
        return

    removed = collection.remove_book(title)
    if removed:
        display_message("\nBook removed successfully.\n")
    else:
        display_message("\nBook not found.\n")


def handle_find():
    print("\nFind Books by Author\n")

    author = input("Author name: ").strip()
    books = collection.find_by_author(author)

    show_books(books)


def show_help():
    print("""
Book Collection Helper

Commands:
  list     - Show all books
  add      - Add a new book
  remove   - Remove a book by title
  find     - Find books by author
  help     - Show this help message
""")


def main():
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1].lower()

    if command == "list":
        handle_list()
    elif command == "add":
        handle_add()
    elif command == "remove":
        handle_remove()
    elif command == "find":
        handle_find()
    elif command == "help":
        show_help()
    else:
        print("Unknown command.\n")
        show_help()


if __name__ == "__main__":
    main()
