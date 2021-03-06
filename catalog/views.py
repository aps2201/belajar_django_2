from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin

# Create your views here.
def index(request):
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    num_instances_available = BookInstance.objects.filter(status__exact = 'a').count()
    num_authors =  Author.objects.count()
    num_genre = Genre.objects.filter(name__exact = 'Fantasy').count()
    num_visits = request.session.get('num_visits',0)
    request.session['num_visits'] = num_visits+1

    return render(
        request,
        'index.html',
        context = {'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors,'num_genre':num_genre,'num_visits':num_visits}
        )


class BookListView(generic.ListView):
    model = Book
    
    
class BookDetailView(generic.DetailView):
    model = Book
    paginate_by = 10


class AuthorListView(generic.ListView):
    model = Author

    
class AuthorDetailView(generic.DetailView):
    model = Author
    paginate_by = 10


class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class AllLoanedBooksListView(PermissionRequiredMixin,generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_all_borrowed_user.html'
    paginate_by = 10
    permission_required = 'catalog.can_mark_returned'
    
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')
