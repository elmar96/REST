from rest_framework import serializers
from .models import Directors,Movie,Review


class DirectorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Directors
        fields = 'id'.split()


class DirectorDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Directors
        fields = '__all__'


class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id'.split()


class ReviewDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class MovieSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = 'id'.split()


class MovieDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

