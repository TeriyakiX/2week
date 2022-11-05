from django.shortcuts import render
from django.views import generic
from .models import Book, Author

def index(request):
    num_books = Book.objects.all().count()
    num_authors = Author.objects.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    return render(
        request,
        'index.html',
        context={'num_books': num_books, 'num_authors': num_authors,
                 'num_visits': num_visits},
    )
