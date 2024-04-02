import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from libmsapp.models import Book, Profile

class Command(BaseCommand):
    help = 'Generate dummy data for books and create user accounts with roles'

    def handle(self, *args, **options):
        # Generate dummy data for books
        book_titles = ["Book 1", "Book 2", "Book 3", "Book 4", "Book 5"]
        for title in book_titles:
            copies = random.randint(1, 5)  
            for _ in range(copies):
                Book.objects.create(title=title, copies=1)

        users_data = [
            {'username': 'anonymous', 'password': 'password', 'user_type': 'Anonymous'},
            {'username': 'student', 'password': 'password', 'user_type': 'Student'},
            {'username': 'librarian', 'password': 'password', 'user_type': 'Librarian'},
        ]
        for user_data in users_data:
            user = User.objects.create_user(username=user_data['username'], password=user_data['password'])
            profile = Profile.objects.create(user=user, user_type=user_data['user_type'])

        self.stdout.write(self.style.SUCCESS('Successfully generated dummy data for books and created user accounts with roles.'))
