from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render, redirect
from .models import Book, BorrowedBook
from .serializers import BookSerializer, BorrowedBookSerializer
from django.contrib.auth.decorators import login_required
from libmsapp.models import BorrowedBook, BookInstance
from libmsapp.models import BookInstance
from datetime import datetime, timedelta

@api_view(['GET'])
def get_books(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_book_availability(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    borrowed_count = BorrowedBook.objects.filter(book=book).count()
    available_copies = book.copies - borrowed_count
    return Response({'available_copies': available_copies})

@api_view(['POST'])
def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if book.copies <= 0:
        return Response({'error': 'No available copies'}, status=400)
    
    borrowed_book = BorrowedBook.objects.create(student=request.user, book=book)
    book.copies -= 1
    book.save()
    serializer = BorrowedBookSerializer(borrowed_book)
    return Response(serializer.data)

@api_view(['DELETE'])
def return_book(request, book_id):
    borrowed_book = get_object_or_404(BorrowedBook, student=request.user, book__id=book_id)
    borrowed_book.delete()
    book = borrowed_book.book
    book.copies += 1
    book.save()
    return Response({'message': 'Book returned successfully'})

@api_view(['PUT'])
def renew_book(request, book_id):
    borrowed_book = get_object_or_404(BorrowedBook, student=request.user, book__id=book_id)
    if borrowed_book.renewal_count >= 1:
        return Response({'error': 'You have already renewed this book once'}, status=400)
    
    borrowed_book.due_date += datetime.timedelta(days=30)
    borrowed_book.renewal_count += 1
    borrowed_book.save()
    serializer = BorrowedBookSerializer(borrowed_book)
    return Response(serializer.data)

@api_view(['GET'])
def get_books(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_book_availability(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    borrowed_count = BorrowedBook.objects.filter(book=book).count()
    available_copies = book.copies - borrowed_count
    return Response({'available_copies': available_copies})

@api_view(['POST'])
def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if book.copies <= 0:
        return Response({'error': 'No available copies'}, status=400)
    
    borrowed_book = BorrowedBook.objects.create(student=request.user, book=book)
    book.copies -= 1
    book.save()
    serializer = BorrowedBookSerializer(borrowed_book)
    return Response(serializer.data)

@api_view(['DELETE'])
def return_book(request, book_id):
    borrowed_book = get_object_or_404(BorrowedBook, student=request.user, book__id=book_id)
    borrowed_book.delete()
    book = borrowed_book.book
    book.copies += 1
    book.save()
    return Response({'message': 'Book returned successfully'})

@api_view(['PUT'])
def renew_book(request, book_id):
    borrowed_book = get_object_or_404(BorrowedBook, student=request.user, book__id=book_id)
    if borrowed_book.renewal_count >= 1:
        return Response({'error': 'You have already renewed this book once'}, status=400)
    
    borrowed_book.due_date += datetime.timedelta(days=30)
    borrowed_book.renewal_count += 1
    borrowed_book.save()
    serializer = BorrowedBookSerializer(borrowed_book)
    return Response(serializer.data)


@login_required
def student_dashboard(request):
    student = request.user
    borrowed_books = BorrowedBook.objects.filter(student=student)
    return render(request, 'student_dashboard.html', {'borrowed_books': borrowed_books})

@login_required
def renew_book(request, book_instance_id):
    book_instance = BookInstance.objects.get(id=book_instance_id)
    if request.method == 'POST':
        # Check if the book is eligible for renewal
        if book_instance.due_back < datetime.now().date():
            return render(request, 'error.html', {'message': 'Book overdue. Cannot renew.'})
        
        # Extend the due date by 7 days
        book_instance.due_back += timedelta(days=7)
        book_instance.save()
        return redirect('student_dashboard')
    return render(request, 'renew_book.html', {'book_instance': book_instance})

@login_required
def librarian_dashboard(request):
    borrowed_books = BorrowedBook.objects.all()
    return render(request, 'librarian_dashboard.html', {'borrowed_books': borrowed_books})

@login_required
def mark_returned(request, borrowed_book_id):
    borrowed_book = BorrowedBook.objects.get(id=borrowed_book_id)
    if request.method == 'POST':
        borrowed_book.returned = True
        borrowed_book.save()
        return redirect('librarian_dashboard')
    return render(request, 'mark_returned.html', {'borrowed_book': borrowed_book})

def check_availability(request, book_id):
    book_instance = BookInstance.objects.filter(book_id=book_id, borrower__isnull=True).first()
    if book_instance:
        copies_available = BookInstance.objects.filter(book_id=book_id, borrower__isnull=True).count()
        return render(request, 'available.html', {'copies_available': copies_available})
    else:
        next_available_date = BookInstance.objects.filter(book_id=book_id).order_by('due_back').first().due_back
        return render(request, 'unavailable.html', {'next_available_date': next_available_date})


def login_page(request):
    if request.user.is_authenticated:
        return redirect('books')
    else:
        return render(request, 'login.html')

@login_required
def books_api(request):
    return render(request, 'books.html')