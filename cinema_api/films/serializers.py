from rest_framework import serializers
from .models import Film, Director, Genre
from rest_framework.exceptions import ValidationError

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class DirectorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['id', 'fio', 'birthday']

# Сериализатор для режиссёра
class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['id', 'fio']


# Сериализатор для фильма в списке
class FilmListSerializer(serializers.ModelSerializer):
    director = DirectorSerializer()  # вложенный сериализатор
    genres = serializers.SerializerMethodField()  # вычисляемое поле

    class Meta:
        model = Film
        fields = ['id', 'title', 'rating', 'is_hit', 'director', 'genres', 'reviews']

    def get_genres(self, film):
        # возвращает список названий жанров
        return film.genre_names


# Детальный сериализатор фильма
class FilmDetailSerializer(serializers.ModelSerializer):
    director = DirectorSerializer()
    genres = serializers.SerializerMethodField()

    class Meta:
        model = Film
        fields = '__all__'

    def get_genres(self, film):
        return film.genre_names
    

class FilmValidateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, max_length=255, min_length=2)
    text = serializers.CharField(required=False)
    rating = serializers.FloatField(min_value=1, max_value=10)
    release_year = serializers.IntegerField()
    is_hit = serializers.BooleanField(default=True)
    director_id = serializers.IntegerField()
    genres = serializers.ListField(child=serializers.IntegerField())

    def validate_director_id(self, director_id):
        try:
            Director.objects.get(id=director_id)
        except Director.DoesNotExist:
            raise ValidationError('Director does not exist!')
        return director_id
    

    def validate_genres(self, genres):
        genres_from_db = Genre.objects.filter(id__in=genres)
        if len(genres_from_db) != len(genres):
            raise ValidationError('Genres does not exist!')
        return genres

    
