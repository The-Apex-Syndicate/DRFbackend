from rest_framework import serializers
from .models import Movie, Genre,ProductionCompany, ProductionCountry, SpokenLanguage, MovieActorMap, Actor, CustomUser, WishList
from datetime import datetime, time
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.exceptions import AuthenticationFailed

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = CustomUser
        ref_name = None
    
    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Incorrect Credentials')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email']

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
    original_language_converted = serializers.SerializerMethodField()
    class Meta:
        model = Movie
        fields = ['id', 'adult', 'genres','original_language', 'original_title', 
                  'overview', 'popularity', 'poster_path', 'production_companies', 'production_countries',
                  'release_date', 'revenue', 'runtime', 'spoken_languages', 'status', 'tagline',
                  'title', 'video','vote_average','vote_count','rating', 'original_language_converted', 'video_url']

    def get_original_language_converted(self, obj):
        if not hasattr(self, '_lang_map'):
            self._lang_map = {l.id: l.name for l in SpokenLanguage.objects.all()}
        return self._lang_map.get(obj.original_language, obj.original_language)

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
                  'title', 'video','vote_average','vote_count','rating', 'cast', 'video_url']


class WishListSerializer(serializers.ModelSerializer):
    movie = serializers.IntegerField()
    class Meta:
        model = WishList
        fields = ['movie']
        depth = 2

    def validate(self, data):
        user = self.context['request'].user
        movie_id = self.context['request'].data.get('movie')
        if not user.is_authenticated:
            raise AuthenticationFailed('Authentication credentials were not provided.')
        
        try:
            movie = Movie.objects.get(id=movie_id)
            data['movie'] = movie  
        except Movie.DoesNotExist:
            raise serializers.ValidationError("Movie does not exist")
        
        if WishList.objects.filter(user=user, movie=movie).exists():
            raise serializers.ValidationError("This movie is already in your wishlist")
        
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        return WishList.objects.create(user=user, **validated_data)
    
    def to_representation(self, instance):
        return MovieListSerializer(instance.movie).data

