from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic

# Create your views here.
def index(request):
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    num_instances_available = BookInstance.objects.filter(status__exact = 'a').count()
    num_authors =  Author.objects.count()
    num_genre = Genre.objects.filter(name__exact = 'Fantasy').count()

    return render(
        request,
        'index.html',
        context = {'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors,'num_genre':num_genre}
        )
class BookListView(generic.ListView):
    model = Book
    
class BookDetailView(generic.DetailView):
    model = Book
