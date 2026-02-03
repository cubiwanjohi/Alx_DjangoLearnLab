from django.contrib import admin
from .models import Book

# Customizing the admin view
class BookAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('title', 'author', 'publication_year')
    
    # Adding filters to the right sidebar
    list_filter = ('author', 'publication_year')
    
    # Adding a search bar at the top
    search_fields = ('title', 'author')

# Register the model with the custom admin class
admin.site.register(Book, BookAdmin)