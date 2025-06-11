from rest_framework import serializers
from .models import Movies
from datetime import datetime, time
from django.conf import settings


def get_all_unique_genres():
    genre_map = {}  

    for movie in Movies.objects.exclude(genres__isnull=True).exclude(genres=[]):
        for genre in movie.genres:
            genre_map[genre['id']] = genre['name']

    genre_list = [{"id": k, "name": v} for k, v in genre_map.items()]
    return genre_list

class MovieListSerializer(serializers.ModelSerializer):

    poster_url = serializers.SerializerMethodField()
    class Meta:
        model = Movies
        fields = ['adult','title','id','release_date', 'popularity', 'vote_average','vote_count','poster_path','poster_url']

    def get_poster_url(self, obj):
        request = self.context.get('request')
        if obj.poster_path:
            print(settings.MEDIA_URL)
            return request.build_absolute_uri(f"{settings.MEDIA_URL}/posters/{obj.id}.jpg")
        return None



class MovieDetailSerializer(serializers.ModelSerializer):
    poster_url = serializers.SerializerMethodField()


    class Meta:
        model = Movies
        fields = ['adult','title','genres','id','release_date', 'popularity', 'vote_average','video','vote_count','poster_path','poster_url']

    def get_poster_url(self, obj):
        request = self.context.get('request')
        if obj.poster_path:
            print(settings.MEDIA_URL)
            return request.build_absolute_uri(f"{settings.MEDIA_URL}/posters/{obj.id}.jpg")
        return None


class GenreSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()