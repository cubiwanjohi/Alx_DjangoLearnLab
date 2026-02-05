from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token  # Import the built-in view
from .views import BookList, BookViewSet

# Create a router and register our viewset with it.
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    # Route for the individual ListAPIView
    path('books/', BookList.as_view(), name='book-list'),
    
    # Route to obtain the authentication token (POST username/password here)
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    
    # Include the router URLs for all CRUD operations
    path('', include(router.urls)),
]