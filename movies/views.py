from django.shortcuts import render
from rest_framework import generics, filters, viewsets
from .serializers import MovieSerializer,GenreSerializer
from .models import Movie, Genre
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django_filters.rest_framework import DjangoFilterBackend
from .filters import MovieFilter



class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all().prefetch_related(
        'genres', 'production_companies', 'production_countries', 'spoken_languages'
    )
    serializer_class = MovieSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MovieFilter
   
class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
