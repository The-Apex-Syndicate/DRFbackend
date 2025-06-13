from django.urls import path
from .views import MovieViewSet,GenreViewSet,MovieActorMapViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('movies', MovieViewSet)
router.register('genres', GenreViewSet)
router.register('movie-actor', MovieActorMapViewSet)


urlpatterns = router.urls


