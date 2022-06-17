from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import MovieSerailizer, MovieDetailSerializers, DirectorSerializers, \
    DirectorDetailSerializers, ReviewSerializers, ReviewDetailSerializers
from .models import Movie, Directors, Review


@api_view(['GET'])
def director_list_view(request):
    directors = Directors.objects.all()
    data = DirectorSerializers(directors, many=True).data
    return Response(data=data)


@api_view(['GET'])
def director_detail_view(request, id):
    directors = Directors.objects.get(id=id)
    data = DirectorDetailSerializers(directors, many=False).data
    return Response(data=data)


@api_view(['GET'])
def review_list_view(request):
    review = Review.objects.all()
    data = ReviewSerializers(review, many=True).data
    return Response(data=data)


@api_view(['GET'])
def review_detail_view(request, id):
    review = Review.objects.get(id=id)
    data = ReviewDetailSerializers(review, many=False).data
    return Response(data=data)


@api_view(['GET'])
def movie_list_view(request):
    movies = Movie.objects.all()
    data = MovieSerailizer(movies, many=True).data
    return Response(data=data)


@api_view(['GET'])
def movie_detail_view(request, id):
    movies = Movie.objects.get(id=id)
    data = MovieDetailSerializers(movies, many=False).data
    return Response(data=data)


@api_view(['GET'])
def static_data_view(request):
    dict_ = {
        'key': 'good'
    }
    return Response(data=dict_)
