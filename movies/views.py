from django.shortcuts import render
from rest_framework import generics, filters, viewsets
from .serializers import GenreSerializer, MovieListSerializer,  MovieDetailSerializer, MovieActorSerializer
from .models import Movie, Genre, MovieActorMap
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django_filters.rest_framework import DjangoFilterBackend
from .filters import MovieFilter



class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        return MovieDetailSerializer
    
    def get_queryset(self):
        queryset = Movie.objects.all().prefetch_related(
            'genres', 'production_companies', 'production_countries', 'spoken_languages'
            ).order_by('-release_date')
        if self.action == 'retrieve':
            queryset = queryset.prefetch_related('cast','cast__actor')
        return queryset

    filter_backends = [DjangoFilterBackend]
    filterset_class = MovieFilter
   
class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class MovieActorMapViewSet(viewsets.ModelViewSet):
    queryset = MovieActorMap.objects.all()
    serializer_class = MovieActorSerializer
