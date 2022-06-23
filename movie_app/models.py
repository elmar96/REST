from django.db import models
from django.db.models import Avg


class Directors(models.Model):
    name = models.CharField(max_length=100)


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    genre = models.ForeignKey(Genre,
                              on_delete=models.CASCADE,
                              null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    duration = models.PositiveIntegerField(null=True)
    director = models.ForeignKey(Directors, on_delete=models.CASCADE,null=True, related_name="directors")

    # def __str__(self):
    #     return self.name

    @property
    def tag_list(self):
        return [i.name for i in self.tags.all()]

    # @property
    # def rate(self):
    #     Movie.objects.aggregate(Avg('rating'))
    #     return


    def rating(self):
        reviews = self.reviews.all()
        if not reviews:
            return 0
        average = 0
        for i in reviews:
            average += i.stars
            return average / reviews.count()


STAR_CHOICES = (
    (1, '*'),
    (2, '**'),
    (3, '***'),
    (4, '****'),
    (5, '*****'),
)


class Review(models.Model):
    text = models.TextField(null=True, blank=True)
    stars = models.IntegerField(default=1, choices=STAR_CHOICES)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return self.text
