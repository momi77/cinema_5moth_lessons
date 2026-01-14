from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Film, Genre, Director
from .serializers import (
DirectorSerializer,
FilmListSerializer,
 FilmDetailSerializer,
 FilmValidateSerializer,
 GenreSerializer,
 DirectorCreateSerializer,

 )
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

class DirectorViewSet(ModelViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DirectorCreateSerializer
        return self.serializer_class

class GenreListAPIView(ListCreateAPIView):
    queryset = Genre.objects.all()  # list of data from DB
    serializer_class = GenreSerializer #sreializer class inherited by ModelSerializer
    pagination_class = PageNumberPagination
    

class GenreDetailAPIView(RetrieveDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'id'


@api_view(['GET','PUT','DELETE'])
def film_detail_api_view(request, id):
    try:
        film = Film.objects.get(id=id)
    except Film.DoesNotExist:
        return Response(data={'error': 'Film not found!'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
       data = FilmDetailSerializer(film, many=False).data
       return Response(data=data)
    elif request.method == 'PUT':
        serializer = FilmValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        film.title = serializer.validated_data.get('title')
        film.text = serializer.validated_data.get('text')
        film.rating = serializer.validated_data.get('rating')
        film.release_year = serializer.validated_data.get('release_year')
        film.is_hit = serializer.validated_data.get('is_hit')
        film.director_id = serializer.validated_data.get('director_id')
        film.genres.set(serializer.validated_data.get('genres'))
        film.save()
        return Response(status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        film.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def film_list_api_view(request):
    if request.method == 'GET':
        # step 1: Collect films from DB(QuerySet)
        films = Film.objects.select_related('director').prefetch_related('reviews', 'genres').all()
        # step 2: Reformat (Serialize) films to list of dictionaries
        data = FilmListSerializer(films, many=True).data
        # step 3: Return Response
        return Response(data=data)
    elif request.method == 'POST':
        # step 0: Validation (existing, typing, extra)
        serializer = FilmValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response (status=status.HTTP_400_BAD_REQUEST,
                             data=serializer.errors)
                

        title = serializer.validated_data.get('title')
        text = serializer.validated_data.get('text')
        rating = serializer.validated_data.get('rating') 
        release_year = serializer.validated_data.get('release_year')
        is_hit = serializer.validated_data.get('is_hit')
        director_id = serializer.validated_data.get('director_id')
        genres = request.data.get('genres')
        print(title, text, rating, release_year, is_hit, sep=' --- ')

        film = Film.objects.create(
            title=title,
            text=text,
            rating=rating,
            release_year=release_year,
            is_hit=is_hit,
            director_id=director_id
        )
        film.genres.set(genres)
        film.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=FilmDetailSerializer(film).data)


