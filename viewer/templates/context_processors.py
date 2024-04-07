import datetime
import random

from viewer.models import Movie, Actor

import logging

req_logger = logging.getLogger('REQUEST_LOGGER')

STATIC_STRINGS = {'hello_message': "Witaj na stronie aplikacji Holly Movies!"}

CIEKAWOSTKI = [""""Powrót do Przyszłości": Reżyser Robert Zemeckis pierwotnie chciał obsadzić Erica Stoltza w roli Marty'ego McFly'a. Dopiero po sześciu tygodniach zdjęć zdecydowano się na Michaela J. Foxa.""",
               """"Titanic": Leonardo DiCaprio początkowo nie chciał zagrać w filmie Jamesa Camerona. Uważał, że historia jest zbyt "miękka". Dopiero po długich namowach reżysera zgodził się na rolę Jacka Dawsona.""",
               """"Gwiezdne Wojny": Darth Vader miał pierwotnie być grany przez Davida Prowse'a, ale jego silny angielski akcent nie pasował do postaci. Głos Vadera podłożył James Earl Jones.""",
               """"Indiana Jones": Harrison Ford nie był pierwszym wyborem do roli Indiany Jonesa. George Lucas rozważał m.in. Toma Sellecka i Steve'a McQueena.""",
               """"Kill Bill": Uma Thurman podczas kręcenia scen walki z Daryl Hannah złamała rękę w dwóch miejscach. Mimo to zdecydowała się dokończyć scenę."""]


def welcome_message(request):
    return STATIC_STRINGS


def ciekawostki(request):
    return {'ciekawostka': random.choice(CIEKAWOSTKI)}


def czas(request):
    return {'data': datetime.datetime.now().date(),
            'czas': datetime.datetime.now().time()}


def num_of_actors_and_movies(request):
    return {'num_of_actors': Actor.objects.count(),
            'num_of_movies': Movie.objects.count()}