from rest_framework import serializers
from .models import Book, Author, Genre

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'
        
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'
        
class BookSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())
    genre = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), many=True)

    class Meta:
        model = Book
        fields = ['id','author', 'genre', 'title', 'published_date']
        
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # Add nested representation for readability in response
        rep['author'] = AuthorSerializer(instance.author).data
        rep['genre'] = GenreSerializer(instance.genre.all(), many=True).data
        return rep
    # def create(self, validated_data):
    #     genres_data = validated_data.pop('genre')
    #     book = Book.objects.create(**validated_data)
    #     for genre_data in genres_data:
    #         genre, created = Genre.objects.get_or_create(**genre_data)
    #         book.genre.add(genre)
    #     return book