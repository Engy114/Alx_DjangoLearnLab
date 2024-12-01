from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, AuthorViewSet, BookListView

# Set up the router for ViewSets
router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'authors', AuthorViewSet, basename='author')

urlpatterns = [
    path('book-list/', BookListView.as_view(), name='book-list'),  # List of all books (read-only)
    path('', include(router.urls)),  # Include ViewSet routes
]

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin site
    path('api/', include('api.urls')),  # Include URLs from the `api` app
]
