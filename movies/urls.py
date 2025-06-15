from django.urls import path
from .views import (MovieViewSet,GenreViewSet,MovieActorMapViewSet,RandomMovieView,
                        ProductionCompanyViewSet,LoginView,SignUpView,WishListViewSet, MovieDetailsListById)
from rest_framework.routers import DefaultRouter
from knox import views as knox_views

router = DefaultRouter()
router.register('movies', MovieViewSet)
router.register('genres', GenreViewSet)
router.register('production-companies', ProductionCompanyViewSet)
router.register('movie-actor', MovieActorMapViewSet)
router.register('wishlist', WishListViewSet)



urlpatterns = router.urls

extra_urls = [
    path('random-movies', RandomMovieView.as_view(), name="random_movies"),
    path('movie_details_list', MovieDetailsListById.as_view(), name="movie_details_list"),
    path('signin', LoginView.as_view(), name="signin"),
    path('signup', SignUpView.as_view(), name="signup"),
    path('signout', knox_views.LogoutView.as_view(), name='knox_logout'),

]
urlpatterns+=extra_urls

