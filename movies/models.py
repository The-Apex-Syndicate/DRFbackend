from django.db import models


class ProductionCompany(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "ProductionCompanies"


class ProductionCountry(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "ProductionCountries"

class Genre(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class SpokenLanguage(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    adult = models.BooleanField(blank=True, null=True, default=False)
    genres = models.ManyToManyField(Genre, related_name='movie_genre', blank=True)
    original_language = models.TextField(blank=True, null=True)
    original_title = models.TextField(blank=True, null=True)
    overview = models.TextField(blank=True, null=True)
    popularity = models.FloatField(blank=True, null=True)
    poster_path = models.TextField(blank=True, null=True)
    production_companies = models.ManyToManyField(ProductionCompany, related_name='movie_production_company', blank=True)
    production_countries = models.ManyToManyField(ProductionCountry, related_name='movie_production_country', blank=True)
    release_date = models.TextField(blank=True, null=True)
    revenue = models.FloatField(blank=True, null=True)
    runtime = models.FloatField(blank=True, null=True)
    spoken_languages = models.ManyToManyField(SpokenLanguage, related_name='movie_spoken_language', blank=True)
    status = models.TextField(blank=True, null=True)
    tagline = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    video = models.BooleanField(blank=True, null=True)
    vote_average = models.FloatField(blank=True, null=True)
    vote_count = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.title

