from django.contrib import admin
from django.urls import path
from movie_app import views
from . import swagger

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/staic_data/", views.StaticDataAPIView.as_view()),
    path("api/v1/movies/", views.MovieListApiView.as_view()),
    path("api/v1/movies/<int:id>/", views.MovieDetailAPIView.as_view()),
    path("api/v1/directors/", views.DirectorListAPIView.as_view()),
    path("api/v1/directors/<int:id>/", views.DirectorDetailAPIView.as_view()),
    path("api/v1/review/", views.ReviewListAPIView.as_view()),
    path("api/v1/review/<int:id>/", views.ReviewDetailAPIView.as_view()),
    path("api/v1/login/", views.LoginAPIView.as_view()),
    path("api/v1/register/", views.RegisterAPIView.as_view()),
    path("api/v1/genres/", views.GenreListAPIView.as_view()),
    path("api/v1/genres/<int:pk>/", views.GenreItemUpdateDeleteAPIView.as_view()),
    path(
        "api/v1/tags/", views.TagModelViewSet.as_view({"get": "list", "post": "create"})
    ),
    path(
        "api/v1/tags/<int:pk>/",
        views.TagModelViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
    ),
]
urlpatterns += swagger.urlpatterns
