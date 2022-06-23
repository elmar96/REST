from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import MovieSerailizer, MovieDetailSerializers, DirectorSerializers, \
    DirectorDetailSerializers, ReviewSerializers, ReviewDetailSerializers
from .models import Movie, Directors, Review


@api_view(['GET','POST'])
def director_list_view(request):
    if request.method == 'GET':
        directors = Directors.objects.all()
        data = DirectorSerializers(directors, many=True).data
        return Response(data=data)
    else:
        name = request.data.get('name')
        director = Directors.objects.create(
            name=name
        )
        director.save()
        return Response(status=status.HTTP_201_CREATED,
                        data={'message': "Director created",
                              "director": DirectorDetailSerializers(name).data})

@api_view(['GET'])
def director_detail_view(request, id):
    directors = Directors.objects.get(id=id)
    data = DirectorDetailSerializers(directors, many=False).data
    return Response(data=data)


@api_view(['GET', 'POST'])
def review_list_view(request):
    if request.method == 'GET':
        review = Review.objects.all()
        data = ReviewSerializers(review, many=True).data
        return Response(data=data)
    else:
        text = request.data.get('text', '')
        stars = request.data.get('stars', 0)
        movie_id = request.data.get('movie_id')
        review = Review.objects.create(
            text=text,
            stars=stars,
            movie_id=movie_id
        )
        review.save()
        return Response(status=status.HTTP_201_CREATED,
                        data={'message': 'Review created',
                              'review':ReviewDetailSerializers(review).data})


@api_view(['GET','PUT','DELETE'])
def review_detail_view(request, id):
    review = Review.objects.get(id=id)
    if request.method == 'GET':
        data = ReviewDetailSerializers(review, many=False).data
        return Response(data=data)
    elif request.method == 'DELETE':
        review.delete()
        return Response(data={'message': "Review removed"})
    else:
        review.text = request.data.get('text')
        review.stars = request.data.get('stars')
        review.movie_id = request.data.get('movie_id')
        review.save()
        return Response(data=ReviewDetailSerializers(review).data)


@api_view(['GET', 'POST'])
def movie_list_view(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        data = MovieSerailizer(movies, many=True).data
        return Response(data=data)
    else:
        title = request.data.get('title', '')
        description = request.data.get("description", "")
        duration = request.data.get("duration", 0)
        genre_id = request.data.get('genre_id')
        tags = request.data.get('tags', [])
        movies = Movie.objects.create(
            title=title,
            description=description,
            duration=duration,
            genre_id=genre_id


        )
        movies.tags.set(tags)
        movies.save()
        return Response(status=status.HTTP_201_CREATED,
                        data={'message': 'Movie created',
                              'movies': MovieDetailSerializers(movies).data})


@api_view(['GET','PUT', 'DELETE'])
def movie_detail_view(request, id):
    try:
        movies = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'error': 'no such movie!'})
    # Получить все отзывы фильтр
    # reviews = movies.reviews.all()
    # Отзывы по фильму ручной филтр
    # reviews = Review.objects.filter(movies=movies)
    movies = Movie.objects.get(id=id)
    if request.method == 'GET':
        data = MovieDetailSerializers(movies, many=False).data
        return Response(data=data)
    elif request.method == 'DELETE':
        movies.delete()
        return Response(data={"message": "Movie removed"})
    else:
        movies.title = request.data.get('title', '')
        movies.description = request.data.get('description')
        movies.duration = request.data.get('duration')
        movies.genre_id = request.data.get('genre_id')
        movies.tags.set(request.data.get('tags', []))
        movies.save()
        return Response(data=MovieDetailSerializers(movies).data )

@api_view(['GET'])
def static_data_view(request):
    dict_ = {
        'key': 'good'
    }
    return Response(data=dict_)
