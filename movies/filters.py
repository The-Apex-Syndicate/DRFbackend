import django_filters
from .models import Movie

class MovieFilter(django_filters.FilterSet):
    explore = django_filters.CharFilter(method='filter_explore', label='Explore')
    title = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Movie
        fields = ['id', 'genres', 'title', 'production_companies', 'explore']  

    def filter_explore(self, queryset, name, value):
        request = self.request  

        if value == 'trending':
            return queryset
        elif value == 'more-like-this':
            movie_id = request.GET.get('movie_id')
            if movie_id:
                try:
                    movie = Movie.objects.get(id=movie_id)
                    genres = movie.genres.all()
                    return queryset.filter(genres__in=genres).exclude(id=movie_id).distinct()
                except Movie.DoesNotExist:
                    return queryset.none()
            return queryset.none()
        elif value == 'recommendation':
            return queryset.order_by('-rating')[:20]
        else:
            return queryset