from books import Book
import json
class Library:
    def __init__(self):
        self.books = {}
    def add_book(self, isbn, title, author, publisher, year): #for if api calls fail for whatever reason
        book = Book(isbn, title, author, publisher, year)
        self.books[isbn] = book
    def remove_book(self, isbn):
        if isbn in self.books:
            self.books.pop(isbn)
            return True
        return False
    def find_by_title(self, title):
        return [self.books[isbn] for isbn in self.books if title.lower() in self.books[isbn].title.lower()]
    def find_by_status(self, status):
        return [self.books[isbn] for isbn in self.books if self.books[isbn].status == status]
    def save(self, filename):
        library_list = []
        for isbn in self.books:
            library_list.append((self.books[isbn].to_dict()))
        with open(filename, "w") as file:
            json.dump(library_list, file)
    def load(self, filename):
        try:
            with open(filename, "r") as file:
                library_list = json.load(file)
        except Exception:
            return False
        for entry in library_list:
            isbn = entry["isbn"] #translating back to our library object by getting the isbn + turning the rest into a book
            book = Book.from_dict(entry)
            self.books[isbn] = book
        return True
    def get_book(self, isbn):
        return self.books.get(isbn)
    def __str__(self):
        book_list = ""
        for index, key in enumerate(self.books):
            book_list += f"{index + 1}. {self.books[key]}\n"
        return book_list
    def book_list(self):
        return list(self.books.values())