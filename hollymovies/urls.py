"""
URL configuration for hollymovies project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path

from django.contrib.auth.models import Permission

from viewer.admin import MovieAdmin, ActorAdmin
from viewer.models import Genre, Movie, Actor, Profile, AccountType
from viewer.views import (
    MoviesAllView,
    MoviesByGenreView,
    StronaGlownaView,
    GenresAllView,
    ActorsAllView,
    MovieCreateView,
    MovieUpdateView,
    MovieDeleteView,
    ActorCreateView,
    ActorUpdateView,
    ActorDeleteView,
    SubmittableLoginView,
    CustomLogoutView,
    SubmittablePasswordChangeView,
    SignUpView,
)

admin.site.register(Genre)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Actor, ActorAdmin)
admin.site.register(Profile)
admin.site.register(AccountType)
admin.site.register(Permission)

# Problem: zrzucanie danych z polskimi znakami do jsona powoduje error kodowania znaku
# Rozwiazanie: python -Xutf8 manage.py dumpdata viewer --output fixtures.json


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', StronaGlownaView.as_view(), name='index'),
    path('accounts/login/', SubmittableLoginView.as_view(), name='login'),
    path('accounts/logout/', CustomLogoutView.as_view(), name='logout'),
    path('accounts/password-change/', SubmittablePasswordChangeView.as_view(), name='password_change'),
    path('accounts/sign-up/', SignUpView.as_view(), name='sign_up'),
    path('movies/', MoviesAllView.as_view(), name='movies'),
    path('movies/<genre>/', MoviesByGenreView.as_view()),
    path('movie/create/', MovieCreateView.as_view(), name='movie_create'),
    path('movie/update/<pk>', MovieUpdateView.as_view(), name='movie_update'),
    path('movie/delete/<pk>', MovieDeleteView.as_view(), name='movie_delete'),
    #TODO: Informacje na temat sluga w URLconf
    path('genres/', GenresAllView.as_view(), name='genres'),
    path('actors/', ActorsAllView.as_view(), name='actors'),
    path('actor/create/', ActorCreateView.as_view(), name='actor_create'),
    path('actor/update/<pk>', ActorUpdateView.as_view(), name='actor_update'),
    path('actor/delete/<pk>', ActorDeleteView.as_view(), name='actor_delete')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
