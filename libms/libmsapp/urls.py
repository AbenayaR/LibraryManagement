from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name='login'),
    path('api/', views.home, name='home'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('librarian/dashboard/', views.librarian_dashboard, name='librarian_dashboard'),
    path('librarian/mark_returned/<int:borrowed_book_id>/', views.mark_returned, name='mark_returned'),
    path('check_availability/<int:book_id>/', views.check_availability, name='check_availability'),
    path('books/', views.get_books, name='get_books'),
    path('books/<int:book_id>/availability/', views.get_book_availability, name='get_book_availability'),
    path('books/<int:book_id>/borrow/', views.borrow_book, name='borrow_book'),
    path('books/<int:book_id>/return/', views.return_book, name='return_book'),
    path('books/<int:book_id>/renew/', views.renew_book, name='renew_book'),
]
