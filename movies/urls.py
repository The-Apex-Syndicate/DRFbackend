from django.urls import path
from .views import MovieViewSet,GenreViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('movies', MovieViewSet)
router.register('genres', GenreViewSet)

urlpatterns = router.urls


