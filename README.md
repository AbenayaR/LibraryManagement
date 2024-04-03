python - m pip install django
django-admin startproject library_site .
python manage.py startapp libmsapp

api

http://127.0.0.1:8000/api/books/1/renew/
http://127.0.0.1:8000/api/books/1/borrow/
http://127.0.0.1:8000/api/books/1/return
http://127.0.0.1:8000/api/books/
python manage.py runserver

URLs for testing:

api/books
api/books/get_books
api/books/1/availability
api/books/2/borrow
api/books/1/return
api/books/1/renew

Approach Used:
--------------------------

Using Django Rest framework with Models, views and Serializers for book and user. Using function based views, have created views for different categories of user as mentioned in the assignment. I have populated only dummy records into the database using shell program inside management folder. Some random values are stored for books and users with profile - Anonymous, Student and Librarian. 

Html templates were included for front end design with functionality implementation for each set of user profiles. When the URL above (as a part of django rest framework) is hit after https://127.0.0.1/api/books, list of all books randomly created will be listed as a response. Created list of copies for the same book and have put the logic for borrow and due date. Once student profile is populated with records, the below functionality can be added to check renewal only once for each student.

To be Implemented after student record addition
------------------------------------------------

from datetime import datetime, timedelta

class Library:
    def __init__(self):
        self.borrowed_books = {}

    def borrow_book(self, student_id, book_name):
        if book_name in self.borrowed_books:
            return "Book is already borrowed."
        else:
            self.borrowed_books[book_name] = {'student_id': student_id, 'borrow_date': datetime.now(), 'renewals': 0}
            return "Book successfully borrowed."

    def renew_book(self, student_id, book_name):
        if book_name in self.borrowed_books:
            current_date = datetime.now()
            due_date = self.borrowed_books[book_name]['borrow_date'] + timedelta(days=30)
            if current_date <= due_date and self.borrowed_books[book_name]['renewals'] < 1:
                self.borrowed_books[book_name]['borrow_date'] = current_date
                self.borrowed_books[book_name]['renewals'] += 1
                return "Book successfully renewed for 30 days."
            else:
                return "Cannot renew. Book already renewed once or past due date."
        else:
            return "Book is not borrowed."

    def check_due_date(self, book_name):
        if book_name in self.borrowed_books:
            due_date = self.borrowed_books[book_name]['borrow_date'] + timedelta(days=30)
            return due_date
        else:
            return "Book is not borrowed."

