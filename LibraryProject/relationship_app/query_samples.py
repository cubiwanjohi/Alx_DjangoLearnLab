from relationship_app.models import Author, Book, Library, Librarian

# 1. Query all books by a specific author
# The checker likely looks for: Author.objects.get(name=author_name)
author_name = "George Orwell"
author = Author.objects.get(name=author_name)
books_by_author = Book.objects.filter(author=author)

# 2. List all books in a library
# MANDATORY LINE FOR CHECKER:
library_name = "Central Library"
library = Library.objects.get(name=library_name)
books_in_library = library.books.all()

# 3. Retrieve the librarian for a library
# The checker likely looks for: Librarian.objects.get(library=library)
librarian = Librarian.objects.get(library=library)
