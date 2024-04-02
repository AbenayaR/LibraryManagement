from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, date

class Book(models.Model):
    title = models.CharField(max_length=100)
    copies = models.IntegerField()

    def available_copies(self):
        return self.copies - self.borrowed_books.count()

    def next_available_date(self):
        if self.borrowed_books.exists():
            return self.borrowed_books.latest('due_date').due_date
        else:
            return None

class BorrowedBook(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrowed_books')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrowed_books')
    due_date = models.DateField()

    def renew(self):
        self.due_date += timedelta(days=7)
        self.save()

class Profile(models.Model):
    USER_TYPES = [
        ('Anonymous', 'Anonymous'),
        ('Student', 'Student'),
        ('Librarian', 'Librarian'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=50, choices=USER_TYPES)

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"

class BookInstance(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    due_back = models.DateField(null=True, blank=True)

    @property
    def is_borrowed(self):
        return self.borrower is not None

    def borrow(self, user):
        if not self.is_borrowed:
            self.borrower = user
            self.save()

    def return_book(self):
        if self.is_borrowed:
            self.borrower = None
            self.save()

    @classmethod
    def available_copies(cls):
        return cls.objects.filter(borrower__isnull=True).count()

    def available_for_anonymous(self):
        if self.is_borrowed:
            next_available_date = self.book.next_available_date()
            return f"This book is currently borrowed. It will be available after {next_available_date}."
        else:
            return f"This book is available to borrow. {self.book.available_copies()} copies are available."

class BorrowingHistory(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_date = models.DateField()
    returned_date = models.DateField(null=True, blank=True)
    renewed = models.BooleanField(default=False)

    @classmethod
    def borrow_history(cls, user):
        return cls.objects.filter(student=user)

    @classmethod
    def borrowed_books(cls, user):
        return cls.objects.filter(student=user, returned_date__isnull=True)

    def mark_returned(self):
        self.returned_date = date.today()
        self.save()

    def mark_renewed(self):
        self.renewed = True
        self.save()
