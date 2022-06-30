from rest_framework import serializers
from .models import Directors, Movie, Review, Genre, Tag
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User

class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "id name".split()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "id name".split()


class MovieSerailizer(serializers.ModelSerializer):
    genre = GenreSerializer()
    tags = TagSerializer(many=True)
    tag_list = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = "id title genre tags rating tag_list".split()

    def get_tag_list(self, movies):
        print(movies)
        return [i.name for i in movies.tags.all()]


class MovieDetailSerializers(serializers.ModelSerializer):
    reviews = ReviewSerializers(many=True)

    class Meta:
        model = Movie
        fields = "id title tags tag_list rating reviews".split()


class DirectorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Directors
        fields = "id name".split()


class DirectorDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Directors
        fields = "__all__"


class ReviewDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"

# class GenreObjectSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     name = serializers.CharField()

class MovieValidateSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField(required=False,default='')
    duration = serializers.FloatField(min_value=0.1)
    genre_id = serializers.IntegerField(allow_null=True, required=False, default=None)
    # genre = GenreObjectSerializer()
    tags = serializers.ListField(child=serializers.IntegerField())

    def validate_genre_id(self,genre_id):
        #Лучще использовать этот метод еогда много обьектов
        # try:
        #     Genre.objects.get(id=genre_id)
        # except Genre.DoesNotExist:
        #     raise ValidationError('Genre not found')
        genres = Genre.objects.filter(id=genre_id)
        if genres.count() == 0:
            raise ValidationError(f"Жанр с идентификационным номером '{genre_id}' не найден!")
        return genre_id

    def validate_tags(self, tags):
        tag_list = Tag.objects.filter(id__in=tags)
        if tag_list.count()!=len(set(tags)):
            raise ValidationError("Tag not found")
        return tags



class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField()
    stars = serializers.IntegerField(min_value=0, max_value=5)
    movie_id = serializers.IntegerField()


class DirectorValidateSerializer(serializers.Serializer):
    name = serializers.CharField()


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate_username(self, username):
        if User.objects.filter(username=username).count()>0:
            raise ValidationError('Пользователь с таким именем уже существует!')
        return username