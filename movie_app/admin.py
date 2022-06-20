from django.contrib import admin
from .models import Directors, Movie, Review, Genre, Tag

admin.site.register(Genre)
admin.site.register(Directors),
admin.site.register(Movie),
admin.site.register(Review),
admin.site.register(Tag)
