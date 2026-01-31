from books import Book
from library import Library
from openlibrary_api import search_book

def safe_int(input):
    if input is not None:
        try:
            return int(input)
        except ValueError:
            return None
    else:
        return None
    
def add_book_handler():
    new_book_input = input("Input the name or ISBN of the book. ")
    book_output = search_book(new_book_input)
    while True:
        print(f"Book found: \n Title: {book_output["title"]}\n Author: {book_output["author"]}\n ISBN: {book_output["isbn"]}\n Publisher: {book_output["publisher"]}\n Year: {book_output["year"]}")
        add_book_command = input("Would you like to modify any of these before saving? Type the field or N to continue. ").lower() #give user opportunity to modify/correct None
        if add_book_command in ["title", "isbn", "publisher", "author", "year"]:
            book_output[add_book_command] = input("What should it be changed to? ")
        elif add_book_command == "n":
            values = book_output.values()
            if None in values or "" in values:
                print("Fields cannot be empty! ") #check there's no Nones
            else:
                print("Book added!")
                return book_output #if all checks are passed return this for the main program to turn into Book
        else:
            print("Invalid command!")

def book_load(book_list):
    length = len(book_list)
    while True:
        for index, item in enumerate(book_list):
            print(f"{index+1}. {item}")
        selection = safe_int(input("Which book would you like to access? 0 to exit. "))
        if 1 <= selection <= length:
            return book_list[selection - 1]
        elif selection == 0:
            break
        else:
            print("invalid input!")
        
def book_menu(book):
    while True:
        print(f"{book.title} by {book.author} ({book.year})\nCurrently {book.status}\nDate Started: {book.date_started}\nDate Finished: {book.date_finished}")
        print("1. View Notes by Page\n2. View Notes by Category\n3. Add Notes\n4. Remove Book\n5. Exit\n")
        command = input("What would you like to do? ")
        if command == "1":
            page_start = input("What page start? Or type 0 to view all notes. ")
            if page_start == 0:
                display_notes(book.notes)
            else:
                page_end = input("What page end? ")
                notes=book.get_notes_by_page_range(page_start,page_end)
                display_notes(notes)
        if command == "2":
            category = input("What category? ")
            notes = book.get_notes_by_category(category)
            display_notes(notes)
        if command == "3":
            page_number = input("What page number? ")
            note = input("Type note: ")
            note_category = input("What category? ")
            if book.add_note(page_number, note, note_category):
                print("Note added! ")
        if command == "4":
            return book.isbn
        if command == "5":
            break

def display_notes(notes):
    print("placeholder")

def main():
    main_library = Library()
    main_library.load("library.json")
    while True:
        command = input("Type your command. \n 1. Book List \n 2. Find Book by Title \n 3. Find Book by Status \n 4. Add New Book \n 5. Quit \n")
        if command == "1":
            book_selection = book_load(main_library.book_list())
            if book_selection is not None:
                remove_isbn = safe_int(book_menu(book_selection))
                if remove_isbn is not None:
                    if main_library.remove_book(f"{remove_isbn}"):
                        print("Book removed.")
        elif command == "2":
            title_search = input("What should we search for? ")
            title_return = main_library.find_by_title(title_search) #returns list of books
            book_selection = book_load(title_return)
            if book_selection is not None:
                remove_isbn = safe_int(book_menu(book_selection)) #loads book, if book loader function returns a number removes that isbn
                if remove_isbn is not None:
                    if main_library.remove_book(f"{remove_isbn}"):
                        print("Book removed.")
        elif command == "3":
            status_search = input("Type read, unread, or reading. ")
            if status_search in ["read", "unread", "reading"]:
                status_return = main_library.filter_by_status(status_search)
                book_selection = book_load(status_return)
                if book_selection is not None:
                    remove_isbn = safe_int(book_menu(book_selection)) #loads book, if book loader function returns a number removes that isbn
                    if remove_isbn is not None:
                        if main_library.remove_book(f"{remove_isbn}"):
                            print("Book removed.")            
            else:
                print("Invalid input!" )
        elif command == "4":
            book = add_book_handler()
            main_library.add_book(book["isbn"], book["title"], book["author"], book["publisher"], book["year"])
            main_library.save("library.json")
        elif command == "5":
            main_library.save("library.json")
            break
        else:
            print("Invalid command! Input a digit only.")
main()