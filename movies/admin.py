from django.contrib import admin
from .models import Movie, Review

# Register your models here.
class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']
admin.site.register(Movie)
admin.site.register(Review)
