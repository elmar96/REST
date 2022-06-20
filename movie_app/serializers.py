from rest_framework import serializers
from .models import Directors, Movie, Review, Genre, Tag


class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = 'id name'.split()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = 'id name'.split()


class MovieSerailizer(serializers.ModelSerializer):
    genre = GenreSerializer()
    tags = TagSerializer(many=True)
    tag_list = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = 'id title genre tags rating tag_list'.split()

    def get_tag_list(self, movies):
        print(movies)
        return [i.name for i in movies.tags.all()]


class MovieDetailSerializers(serializers.ModelSerializer):
    reviews = ReviewSerializers(many=True)

    class Meta:
        model = Movie
        fields = 'id title tags tag_list rating reviews'.split()


class DirectorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Directors
        fields = 'id'.split()


class DirectorDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Directors
        fields = '__all__'


class ReviewDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
