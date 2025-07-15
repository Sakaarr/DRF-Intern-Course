from django.urls import path
from .views import BlogListCreateView, BlogDetailView


urlpatterns = [
    path('blogs/', BlogListCreateView.as_view(), name='blog-list'),  # URL for listing and creating blogs
    path('blogs/<int:pk>/', BlogDetailView.as_view(), name='blog-detail'),  # URL for retrieving, updating, and deleting a specific blog
]

# 127.0.0.1:8000/api/blogs/