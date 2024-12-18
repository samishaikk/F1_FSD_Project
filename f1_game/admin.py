from django.contrib import admin
from .models import Driver, Car, Engineer
from .models import RacePosition

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost', 'skill')
    search_fields = ('name',)

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost', 'performance')
    search_fields = ('name',)

@admin.register(Engineer)
class EngineerAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost', 'strategy')
    search_fields = ('name',)
