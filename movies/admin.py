from django.contrib import admin
from .models import Movie, ProductionCompany, ProductionCountry, Genre, SpokenLanguage

admin.site.register(Movie)
admin.site.register(ProductionCompany)
admin.site.register(ProductionCountry)
admin.site.register(Genre)
admin.site.register(SpokenLanguage)

