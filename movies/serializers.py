from rest_framework import serializers
from .models import Movies
from datetime import datetime, time
from django.conf import settings




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