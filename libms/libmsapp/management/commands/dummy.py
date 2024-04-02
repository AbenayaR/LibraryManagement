# libmsapp/management/commands/populate_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from libmsapp.models import Book, BorrowedBook
import random
from datetime import timedelta, datetime

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # Create users
        for i in range(5):
            User.objects.create_user(username=f'user{i}', password='password')

        for i in range(10):
            Book.objects.create(title=f'Book {i}', copies=random.randint(1, 10))

        users = User.objects.all()
        books = Book.objects.all()
        for i in range(20):
            user = random.choice(users)
            book = random.choice(books)
            due_date = datetime.now() + timedelta(days=random.randint(1, 30))
            BorrowedBook.objects.create(student=user, book=book, due_date=due_date)

        self.stdout.write(self.style.SUCCESS('Some dummy records are added for testing'))
