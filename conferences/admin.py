from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from .models import conference
from django.utils import timezone
from users.models import *
from django.db.models import Count

# Register your models here.

class ReservationInline(admin.TabularInline):
    model = reservation
    extra = 1
    readonly_fields = ('reservation_date',)
    can_delete = True

class ConferenceDateFilter(admin.SimpleListFilter):
    title = "Date de la conférence"
    parameter_name = "conference_date"

    def lookups(self, request, model_admin):
        return (
            ('past', 'Conférences passées'),
            ('today', 'Conférences aujourd\'hui'),
            ('upcoming', 'Conférences à venir'),
        )

    def queryset(self, request, queryset):
        today = timezone.now().date()
        if self.value() == 'past':
            return queryset.filter(end_date__lt=today)
        if self.value() == 'today':
            return queryset.filter(start_date=today)
        if self.value() == 'upcoming':
            return queryset.filter(start_date__gt=today)
        return queryset

class ParticipantFilter(admin.SimpleListFilter):
    title = "Filtre par participants"
    parameter_name = "participants"

    def lookups(self, request, model_admin):
        return (
            ('0', 'Aucun participant'),
            ('more', 'Avec participants'),
        )

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.annotate(participant_count=Count('reservations')).filter(participant_count=0)
        if self.value() == 'more':
            return queryset.annotate(participant_count=Count('reservations')).filter(participant_count__gt=0)
        return queryset

class ConferenceAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'start_date', 'end_date', 'price')
    list_editable = ('start_date', 'end_date')

    search_fields = ('title',)
    list_per_page = 3
    ordering = ('start_date', 'title')
    
    fieldsets = (
        ('Description', {
            'fields': ('title', 'description', 'category', 'location', 'price', 'capacity')
        }),
        ('Horaires', {
            'fields': ('start_date', 'end_date')
        }),
        ('Documents', {
            'fields': ('program',)
        }),
    )
    
    readonly_fields = ('created_at', 'update_at')
    inlines = [ReservationInline]
    autocomplete_fields = ('category',)
    list_filter = ('title', ParticipantFilter, ConferenceDateFilter)

admin.site.register(conference, ConferenceAdmin)
