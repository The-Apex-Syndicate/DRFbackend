from django.db import models


class ProductionCompany(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(blank=True, null=True, max_length=300)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "ProductionCompanies"


class ProductionCountry(models.Model):
    id = models.TextField(primary_key=True)
    name = models.CharField(blank=True, null=True, max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "ProductionCountries"

class Genre(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(blank=True, null=True, max_length=100)

    def __str__(self):
        return self.name

class SpokenLanguage(models.Model):
    id = models.TextField(primary_key=True)
    name = models.CharField(blank=True, null=True, max_length=100)

    def __str__(self):
        return self.name

class Actor(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(blank=True, null=True, max_length=100)
    gender = models.IntegerField()

    def __str__(self):
        return self.name
    

    
class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    adult = models.BooleanField(blank=True, null=True, default=False)
    genres = models.ManyToManyField(Genre, related_name='movie_genre', blank=True)
    original_language = models.CharField(blank=True, null=True, max_length=5)
    original_title = models.CharField(blank=True, null=True, max_length=300)
    overview = models.TextField(blank=True, null=True)
    popularity = models.FloatField(blank=True, null=True)
    poster_path = models.CharField(blank=True, null=True, max_length=200)
    production_companies = models.ManyToManyField(ProductionCompany, related_name='movie_production_company', blank=True)
    production_countries = models.ManyToManyField(ProductionCountry, related_name='movie_production_country', blank=True)
    release_date = models.DateField(blank=True, null=True)
    revenue = models.FloatField(blank=True, null=True)
    runtime = models.FloatField(blank=True, null=True)
    spoken_languages = models.ManyToManyField(SpokenLanguage, related_name='movie_spoken_language', blank=True)
    status = models.CharField(blank=True, null=True, max_length=20)
    tagline = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True, max_length=300)
    video = models.BooleanField(blank=True, null=True)
    vote_average = models.FloatField(blank=True, null=True)
    vote_count = models.FloatField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.title


class MovieActorMap(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='cast')
    actor = models.ForeignKey(Actor, on_delete=models.DO_NOTHING)
    character_name = models.CharField(blank=True, null=True, max_length=300)
    profile_path = models.CharField(blank=True, null=True, max_length=200)

    def __str__(self):
        return f'{self.movie.title}'

    class Meta:
        unique_together = ['movie', 'actor', 'character_name']
    