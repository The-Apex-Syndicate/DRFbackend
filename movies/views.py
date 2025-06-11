from django.shortcuts import render
from rest_framework import generics, filters
from .serializers import MovieListSerializer, MovieDetailSerializer, GenreSerializer, get_all_unique_genres
from .models import Movies
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank


# Create your views here.


class MoviePagination(PageNumberPagination):
    page_size = 25  # customize page size here
    page_size_query_param = 'page_size'  # allow client to override with ?page_size=xyz
    max_page_size = 50

class MovieListView(generics.ListAPIView):
    serializer_class = MovieListSerializer
    pagination_class = MoviePagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['release_date', 'title', 'popularity']
    ordering = ['id']

    def get_queryset(self):
        query = self.request.GET.get('search', '')
        if query:
            vector = (
                SearchVector('title', weight='A') 
                # SearchVector('overview', weight='B')
            )
            search_query = SearchQuery(query)
            return Movies.objects.annotate(
                rank=SearchRank(vector, search_query)
            ).filter(rank__gt=0).order_by('-rank')
        return Movies.objects.all()




class MovieDetailView(generics.RetrieveAPIView):
    queryset = Movies.objects.all()
    serializer_class = MovieDetailSerializer




class CategoryListView(generics.GenericAPIView):

    queryset = Movies.objects.all()
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get(self, request):
        genres = get_all_unique_genres()
        return Response(genres)