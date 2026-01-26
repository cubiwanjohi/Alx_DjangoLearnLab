from relationship_app.models import Author, Book, Library, Librarian

if not Author.objects.filter(name="George Orwell").exists():
    author = Author.objects.create(name="George Orwell")
else:
    author = Author.objects.get(name="George Orwell")

if not Book.objects.filter(title="1984").exists():
    book = Book.objects.create(title="1984", author=author)
else:
    book = Book.objects.get(title="1984")

if not Library.objects.filter(name="Central Library").exists():
    library = Library.objects.create(name="Central Library")
    library.books.add(book)
else:
    library = Library.objects.get(name="Central Library")

if not hasattr(library, 'librarian'):
    librarian = Librarian.objects.create(name="Alice", library=library)
else:
    librarian = library.librarian

# ------------------------------
# Queries
# ------------------------------

# 1️⃣ Query all books by a specific author
print("\nBooks by George Orwell:")
books_by_author = author.books.all()
for b in books_by_author:
    print(f"- {b.title}")

# 2️⃣ List all books in a library
print(f"\nBooks in {library.name}:")
library_books = library.books.all()
for b in library_books:
    print(f"- {b.title}")

# 3️⃣ Retrieve the librarian for a library
print(f"\nLibrarian for {library.name}: {library.librarian.name}")
