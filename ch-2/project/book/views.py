from django.shortcuts import render
from rest_framework import generics
# Create your views here.
from .models import Book, Author, Genre
from .serializers import BookSerializer, AuthorSerializer, GenreSerializer  
from drf_spectacular.utils import extend_schema


@extend_schema(request=BookSerializer, responses=BookSerializer)
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
@extend_schema(request=BookSerializer, responses=BookSerializer)
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
@extend_schema(request=AuthorSerializer, responses=AuthorSerializer)
class AuthorListCreateView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    
@extend_schema(request=AuthorSerializer, responses=AuthorSerializer)
class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):  
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    
@extend_schema(request=GenreSerializer, responses=GenreSerializer)
class GenreListCreateView(generics.ListCreateAPIView):  
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    
@extend_schema(request=GenreSerializer, responses=GenreSerializer)
class GenreDetailView(generics.RetrieveUpdateDestroyAPIView):       
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer