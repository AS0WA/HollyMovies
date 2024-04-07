from logging import getLogger

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView

from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView
)

# TODO: TemplateView renderuje template raz a potem nie reaguje na zmiany w bazie danych modeli - do poprawienia?

from django.urls import reverse_lazy, reverse

from viewer.models import Movie, Genre, Actor
from viewer.forms import MovieForm, ActorForm, SignUpForm


LOGGER = getLogger()
LOGGER.setLevel('INFO')


def viewer_403_handler(request, exception, template_name='403.html'):
    print("Exception:", exception)
    response = render(request, template_name)
    response.status_code = 403
    return response


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class MoviesAllView(ListView):
    template_name = 'movies.html'
    model = Movie

    def post(self, request):
        if request.POST.get('create') is not None:
            return redirect(reverse('movie_create'))
        elif request.POST.get('update') is not None:
            return redirect(reverse('movie_update', args=[request.POST.get('update')]))
        elif request.POST.get('delete') is not None:
            return redirect(reverse('movie_delete', args=[request.POST.get('delete')]))
        else:
            return redirect(reverse('index'))


class GenresAllView(ListView):
    template_name = 'generic.html'
    model = Genre


class ActorsAllView(ListView):
    template_name = 'actors.html'
    model = Actor

    def post(self, request):
        if request.POST.get('create') is not None:
            return redirect(reverse('actor_create'))
        elif request.POST.get('update') is not None:
            return redirect(reverse('actor_update', args=[request.POST.get('update')]))
        elif request.POST.get('delete') is not None:
            return redirect(reverse('actor_delete', args=[request.POST.get('delete')]))
        else:
            return redirect(reverse('index'))


class StronaGlownaView(View):
    def get(self, request):
        return render(
            request, template_name='index.html',
            context={}
        )


class MovieSelection(View):
    def get(self, request):

        movies = Movie.objects.all()

        return render(
            request, template_name='movie_selection.html',
            context={'movies': movies}
        )

    def post(self, request):
        if request.POST.get('create') is not None:
            return redirect(reverse('movie_create'))
        elif request.POST.get('update') is not None:
            return redirect(reverse('movie_update', args=[request.POST.get('update')]))
        elif request.POST.get('delete') is not None:
            return redirect(reverse('movie_delete', args=[request.POST.get('delete')]))
        else:
            return redirect(reverse('index'))


class MoviesByGenreView(View):
    def get(self, request, genre):
        # movies = Movie.objects.filter(genre__name=genre)

        # movies = Movie.objects.filter(genre__name__iexact=genre)

        movies = []
        for movie in Movie.objects.all():
            if movie.genre.name.lower() == genre.lower():
                movies.append(movie)

        return render(
            request, template_name='movies.html',
            context={'movies': movies}
        )


class MovieCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'form.html'
    # template_name = 'model.html'
    form_class = MovieForm
    success_url = reverse_lazy('movies')
    permission_required = 'viewer.add_movie'

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid(form)


class MovieUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'form.html'
    # template_name = 'model.html'
    model = Movie
    form_class = MovieForm
    success_url = reverse_lazy('movies')
    permission_required = 'viewer.change_movie'

    def form_invalid(self, form):
        LOGGER.warning('User provided incorrect data while updating movie.')
        return super().form_invalid(form)


class MovieDeleteView(LoginRequiredMixin, StaffRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'movie_confirm_delete.html'
    model = Movie
    success_url = reverse_lazy('movies')
    permission_required = 'viewer.delete_movie'

    def post(self, request, *args, **kwargs):

        button_url = request.POST.get('button')

        # Wymaganie 1: W przypadku wciśnięcia przycisku - nie chce usuwać filmu -
        # wróc do strony głównej bez usuwania filmu
        # Klient zmienił zdanie - chce wrócić do wyboru filmu
        if button_url == "movie_select":  # Akcja wciśnięcia przycisku, która przyszła do nas
            # z frontu (my jesteśmy backendem)
            return redirect(reverse('movie_selection'))

        return super().post(request, *args, **kwargs)


class ActorCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'form.html'
    # template_name = 'model.html'
    form_class = ActorForm
    success_url = reverse_lazy('actors')
    permission_required = 'viewer.add_actor'


    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid(form)


class ActorUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'form.html'
    # template_name = 'model.html'
    model = Actor
    form_class = ActorForm
    success_url = reverse_lazy('actors')
    permission_required = 'viewer.change_actor'

    def form_invalid(self, form):
        LOGGER.warning('User provided incorrect data while updating actor.')
        return super().form_invalid(form)


class ActorDeleteView(LoginRequiredMixin, StaffRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'actor_confirm_delete.html'
    model = Actor
    success_url = reverse_lazy('actors')
    permission_required = 'viewer.delete_actor'


class SubmittableLoginView(LoginView):
    template_name = 'form.html'


class CustomLogoutView(LogoutView):
    template_name = 'accounts/logout.html'


class SubmittablePasswordChangeView(PasswordChangeView):
    template_name = 'form.html'
    success_url = reverse_lazy('index')


class SignUpView(CreateView):
    template_name = 'form.html'
    form_class = SignUpForm
    success_url = reverse_lazy('index')


"""

ZADANIE 14:
    a) Stworz nastepujace grupy:
        - ogladajacy (moze ogladac filmy/aktorow) --> 'viewer.view_movie'/'viewer.view_actor'
        - kurator_filmow (moze dodawac/modyfikowac filmy)
        - kurator_aktorow (moze dodawac/modyfikowac aktorow)
        - moderator (moze usuwac filmy lub aktorow)

    b) Stworzcie kilku nowych uzytkownikow i dajcie im rozne uprawnienia.
        - np Ania - kuratorka filmow
        - Stefan - kurator_aktorow oraz moderator
        - Wiesiek - moderator

    c) Na panelu po lewej stronie stworz informacje o przynaleznosci uzytkownika do danych grup.

        {% user.groups %}

"""
