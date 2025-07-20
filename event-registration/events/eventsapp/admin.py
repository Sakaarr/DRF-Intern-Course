from django.contrib import admin
from .models import Event, UserRegistration
# Register your models here.

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'location', 'capacity', 'total_registrations')
    search_fields = ('title', 'location')
    list_filter = ('start_date', 'end_date')
    
@admin.register(UserRegistration)
class UserRegistrationAdmin(admin.ModelAdmin):
    list_display = ('event', 'name', 'email', 'phone', 'registered_at')
    search_fields = ('name', 'email', 'event__title')
    list_filter = ('event', 'registered_at')