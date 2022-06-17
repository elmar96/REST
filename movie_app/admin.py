from django.contrib import admin
from .models import Directors,Movie,Review

admin.site.register(Directors),
admin.site.register(Movie),
admin.site.register(Review)