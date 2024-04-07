from django.contrib.admin import ModelAdmin
from viewer.models import Actor


class MovieAdmin(ModelAdmin):

    @staticmethod
    def released_year(obj):
        return obj.release_date.year

    @staticmethod
    def cleanup_description(modeladmin, request, queryset):
        queryset.update(description='Wyczyszczone przez administratora')

    ordering = ['id']
    list_display = ['id', 'title', 'genre', 'released_year']
    list_display_links = ['id', 'title']
    list_per_page = 20
    list_filter = ['genre']
    search_fields = ['title']
    actions = ['cleanup_description']

    readonly_fields = ['created_entry']

    fieldsets = [
        (None, {'fields': ['title', 'created_entry']}),
        (
            'External Information',
            {
                'fields': ['genre', 'release_date'],
                'description': 'These fields are going to be filled with data parsed from external databases.'
            }
        ),
        (
            'User Information',
            {
                'fields': ['rating', 'description'],
                'description': 'These fields are going to be filled by user'
            }
        )
    ]


class ActorAdmin(ModelAdmin):

    @staticmethod
    def birth_date(obj):
        return obj.birth_date.year

    @staticmethod
    def award_an_oscar(modeladmin, request, queryset):
        for actor in queryset:
            awards = actor.awards
            if awards:
                awards += ', OSKAR'
            else:
                awards = 'OSKAR'
            actor.awards = awards
            actor.save()

    ordering = ['id']
    list_display = ['id', 'name', 'surname', 'birth_date', 'age']
    list_display_links = ['id', 'name', 'surname']
    list_per_page = 20
    search_fields = ['name']
    actions = ['award_an_oscar']

    readonly_fields = ['age']

    fieldsets = [
        (None, {'fields': ['name', 'surname']}),
        (
            'External Information',
            {
                'fields': ['awards'],
                'description': 'These fields are going to be filled with data parsed from external databases.'
            }
        ),
        (
            'User Information',
            {
                'fields': ['birth_date', 'place_of_birth'],
                'description': 'These fields are going to be filled by user'
            }
        )
    ]
