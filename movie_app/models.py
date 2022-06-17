from django.db import models


class Directors(models.Model):
    name = models.CharField(max_length=100)


class Movie(models.Model):
    title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    duration = models.PositiveIntegerField()
    director = models.ForeignKey(Directors, on_delete=models.CASCADE, related_name="directors")


class Review(models.Model):
    text = models.TextField(null=True, blank=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movies')
