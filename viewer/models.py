from django.db.models import (
    Model,
    CharField,
    DateField,
    DateTimeField,
    ForeignKey,
    IntegerField,
    TextField,
    BooleanField,
    CASCADE,
    DO_NOTHING
)

from django.contrib.auth.models import AbstractUser


class AccountType(Model):
    type = CharField(max_length=64)

    def __str__(self):
        return self.type


class Genre(Model):
    name = CharField(max_length=128)

    def __str__(self):
        return self.name


class Movie(Model):
    title = CharField(max_length=128)
    genre = ForeignKey(Genre, on_delete=DO_NOTHING)
    rating = IntegerField()
    release_date = DateField()
    description = TextField(blank=True)
    created_entry = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Actor(Model):
    name = CharField(max_length=64)
    surname = CharField(max_length=64)
    birth_date = DateField()
    age = IntegerField(blank=True)
    awards = TextField()
    place_of_birth = CharField(max_length=128)

    def __str__(self):
        return f"{self.name} {self.surname}"


class Profile(AbstractUser):
    biography = TextField(blank=True)
    is_director = BooleanField(null=True)
    account_type = ForeignKey(AccountType, on_delete=CASCADE, blank=True)

    instagram_link = CharField(max_length=128, null=True)
    linkedin_link = CharField(max_length=128, null=True)

    # W przypadku tworzenia nowego uzytkownika, nadajemy mu wartosc account_type na 'regular'
    # Jezeli tej wartosci nie ma w bazie - chcemy ja stworzyc
    def save(self, *args, **kwargs):
        self.account_type, create = AccountType.objects.get_or_create(
            type='regular',
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


"""
ZADANIE 13:
  Stworzcie nowy defaultowy model użytkownika który dziedziczy po
  AbstractUser i posiada następujące pola:
  1. IsActor   *** DLA CHETNYCH -> Jezeli uzytkownik wybierze, ze jest aktorem
                    to niech dostanie liste filmow z bazy danych i moze sobie wybrac
                    w ktorych grał
"""