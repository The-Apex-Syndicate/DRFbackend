from django.shortcuts import render
from rest_framework import generics, filters, viewsets, mixins
from .serializers import (GenreSerializer, MovieListSerializer, MovieDetailSerializer, MovieActorSerializer, 
ProductionCompanySerializer, LoginSerializer, UserSerializer,RegisterSerializer, WishListSerializer)
from .models import Movie, Genre, MovieActorMap, ProductionCompany, WishList
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django_filters.rest_framework import DjangoFilterBackend
from .filters import MovieFilter
from django.db.models import F  
from rest_framework.views import APIView
import random
from django.contrib.auth import authenticate, login
from knox.models import AuthToken
from knox.auth import TokenAuthentication


class SignUpView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = AuthToken.objects.create(user)
        return Response({
            "user": UserSerializer(user).data,
            "token": token[1]
        })
    
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user).data,
            "token": AuthToken.objects.create(user)[1]
        })

class MovieViewSet(viewsets.GenericViewSet,mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Movie.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        return MovieDetailSerializer
    
    def get_queryset(self):
        queryset = Movie.objects.all().prefetch_related(
            'genres', 'production_companies', 'production_countries', 'spoken_languages'
            ).order_by(F('release_date').desc(nulls_last=True))
        if self.action == 'retrieve':
            queryset = queryset.prefetch_related('cast','cast__actor')
        return queryset

    filter_backends = [DjangoFilterBackend]
    filterset_class = MovieFilter
   
class GenreViewSet(viewsets.GenericViewSet,mixins.ListModelMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class ProductionCompanyViewSet(viewsets.GenericViewSet,mixins.ListModelMixin):
    queryset = ProductionCompany.objects.all()
    serializer_class = ProductionCompanySerializer
    

class MovieActorMapViewSet(viewsets.GenericViewSet,mixins.ListModelMixin):
    queryset = MovieActorMap.objects.all()
    serializer_class = MovieActorSerializer

class RandomMovieView(APIView):
    def get(self, request):
        movie_ids = list(Movie.objects.values_list('id', flat=True))
        random_ids=random.sample(movie_ids, 3)
        movies = Movie.objects.filter(id__in=random_ids).prefetch_related(
            'genres', 'production_companies', 'production_countries', 'spoken_languages'
            )
        serialized_movies = MovieListSerializer(movies, many=True)
        return Response(serialized_movies.data)

class WishListViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    queryset = WishList.objects.all().select_related('movie', 'user').order_by('-created_at')
    serializer_class = WishListSerializer
    
    def get_queryset(self):
        return WishList.objects.filter(user=self.request.user).select_related('movie', 'user').order_by('-created_at')

    def destroy(self, request, *args, **kwargs):
        try:
            movie_id = kwargs.get('pk')
            wishlist_item = WishList.objects.get(
                user=request.user,
                movie_id=movie_id
            )            
            wishlist_item.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except WishList.DoesNotExist:
            return Response(
                {"error": "Wishlist item not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

  
class MovieDetailsListById(APIView):
    def get(self, request):
        movie_ids = request.query_params.getlist('id')
        if not movie_ids:
            return Response({"detail": "No movie id provided."}, status=status.HTTP_400_BAD_REQUEST)
        movies = Movie.objects.filter(id__in=movie_ids)
        if not movies.exists():
            return Response({"detail": "No movies found"}, status=status.HTTP_404_NOT_FOUND)        
        serializer = MovieListSerializer(movies, many=True)        
        return Response(serializer.data, status=status.HTTP_200_OK)