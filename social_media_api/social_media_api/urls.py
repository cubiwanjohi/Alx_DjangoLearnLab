from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.py),
    path('api/accounts/', include('accounts.urls')),
    path('api/', include('posts.urls')), 
]