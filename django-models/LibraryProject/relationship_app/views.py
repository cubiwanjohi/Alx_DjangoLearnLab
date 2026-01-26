from django.shortcuts import render
from django.views.generic.detail import DetailView
from bookshelf.models import Book, Library  # adjust imports to your actual models

# --------------------------
# Function-Based View
# --------------------------
def list_books(request):
    """
    Renders a simple text list of all books and their authors.
    """
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


# --------------------------
# Class-Based View
# --------------------------
class LibraryDetailView(DetailView):
    """
    Displays details for a specific library, listing all books in it.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
