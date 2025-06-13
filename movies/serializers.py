from rest_framework import serializers
from .models import Movie, Genre,ProductionCompany, ProductionCountry, SpokenLanguage, MovieActorMap, Actor
from datetime import datetime, time
from django.conf import settings


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class ProductionCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionCompany
        fields = ['id', 'name']

class ProductionCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionCountry
        fields = ['id', 'name']

class SpokenLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpokenLanguage
        fields = ['id', 'name']

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['id', 'name', 'gender']

class MovieActorSerializer(serializers.ModelSerializer):
    actor = ActorSerializer()      
    class Meta:
        model = MovieActorMap
        fields = ['actor','character_name', 'profile_path']
        
class MovieListSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    production_companies = ProductionCompanySerializer(many=True, read_only=True)
    production_countries = ProductionCountrySerializer(many=True, read_only=True)
    spoken_languages = SpokenLanguageSerializer(many=True, read_only=True)
    class Meta:
        model = Movie
        fields = '__all__'

class MovieDetailSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    production_companies = ProductionCompanySerializer(many=True, read_only=True)
    production_countries = ProductionCountrySerializer(many=True, read_only=True)
    spoken_languages = SpokenLanguageSerializer(many=True, read_only=True)
    cast = MovieActorSerializer(many=True, read_only=True)
    class Meta:
        model = Movie
        fields = ['id', 'adult', 'genres','original_language', 'original_title', 
                  'overview', 'popularity', 'poster_path', 'production_companies', 'production_countries',
                  'release_date', 'revenue', 'runtime', 'spoken_languages', 'status', 'tagline',
                  'title', 'video','vote_average','vote_count','rating', 'cast']



