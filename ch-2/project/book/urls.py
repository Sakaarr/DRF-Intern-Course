from django.urls import path
from .views import AuthorDetailView, AuthorListCreateView, BookDetailView,BookListCreateView, GenreListCreateView, GenreDetailView


urlpatterns = [
    path('author/', AuthorListCreateView.as_view(), name='author-list'),  # URL for listing and creating blogs
    path('author/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),  # URL for retrieving, updating, and deleting a specific blog
    path('books/', BookListCreateView.as_view(), name='book-list'),  # URL for listing and creating blogs
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),  # URL for retrieving, updating, and deleting a specific blog
    path('genre/', GenreListCreateView.as_view(), name='genre-list'),  # URL for listing and creating blogs
    path('genre/<int:pk>/', GenreDetailView.as_view(), name='genre-detail'),  # URL for retrieving, updating, and deleting a specific blog
]
