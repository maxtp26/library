from datetime import datetime

def safe_int(page):
    try:
        return int(page)
    except ValueError:
        return None
    
class Book:
    def __init__(self, isbn, title, author, publisher, year):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.publisher = publisher
        self.year = year
        self.status = "unread"
        self.date_started = None
        self.date_finished = None
        self.notes = []
    def mark_unread(self):
        self.date_started = None
        self.date_finished = None
        self.status = "unread"
    def mark_reading(self, date_started=None):
        if date_started is None:
            self.date_started = datetime.now().strftime("%Y-%m-%d")
        else:
            self.date_started = date_started
        self.status = "reading"
    def mark_finished(self, date_finished=None):
        if date_finished is None:
            self.date_finished = datetime.now().strftime("%Y-%m-%d")
        else:
            self.date_finished = date_finished
        self.status = "read"
    def add_note(self, page, content, category):
        page_num = safe_int(page)
        if page_num is not None:
            self.notes.append({"page": page_num, "content": content, "category": category})
            return True
        else:
            return False
    def change_note(self, index, content, category):
        index_int = safe_int(index)
        if index_int is not None:
            if 0 <= index_int < len(self.notes):
                self.notes[index_int]["content"] = content
                self.notes[index_int]["category"] = category
                return True
        return False
    def remove_note(self, index):
        index_int = safe_int(index)
        if index_int is not None:
            if 0 <= index_int < len(self.notes):
                self.notes.pop(index_int)
                return True
        return False
    def to_dict(self):
        return {
            "isbn": self.isbn,
            "title": self.title,
            "author": self.author,
            "publisher": self.publisher,
            "year": self.year,
            "status": self.status,
            "date_started": self.date_started,
            "date_finished": self.date_finished,
            "notes": self.notes
        }
    @classmethod
    def from_dict(cls, dict):
        book = Book(dict["isbn"], dict["title"], dict["author"], dict["publisher"], dict["year"])
        book.status = dict["status"]
        book.date_started = dict["date_started"]
        book.date_finished = dict["date_finished"]
        book.notes = dict["notes"]
        return book
    def get_notes_by_category(self, category):
        return [note for note in self.notes if note["category"] == category]
    def get_notes_by_page_range(self, start, end):
        page_start = safe_int(start)
        page_end = safe_int(end)
        if page_start is not None and page_end is not None and page_end >= page_start:
            return [note for note in self.notes if note["page"] >= page_start and note["page"] <= page_end]
        else:
            return False
    def __str__(self):
        return f"{self.title} by {self.author}, {self.year}"