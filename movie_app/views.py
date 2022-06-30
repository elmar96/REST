from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response


from .models import Movie, Directors, Review
from .serializers import (
    MovieSerailizer,
    MovieDetailSerializers,
    DirectorSerializers,
    DirectorDetailSerializers,
    ReviewSerializers,
    ReviewDetailSerializers,
    MovieValidateSerializer,
    DirectorValidateSerializer,
    ReviewValidateSerializer,
    UserLoginSerializer,
    UserCreateSerializer
)
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
def register_view(request):

    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = User.objects.create_user(**serializer.validated_data)
    return Response(status=status.HTTP_201_CREATED,
                    data={'user_id':user.id})

@api_view(['POST'])
def login_view(request):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = authenticate(**serializer.validated_data)
    if user is not None:
        try:
            token = Token.objects.get(user=user)
        except:
            token = Token.objects.create(user=user)

            token = Token.objects.create(user=user)
        return Response(data={'key': token.key})
    return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(["GET", "POST"])
def director_list_view(request):
    if request.method == "GET":
        directors = Directors.objects.all()
        data = DirectorSerializers(directors, many=True).data
        return Response(data=data)
    else:
        serializer = DirectorValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_406_NOT_ACCEPTABLE,
                data={"errors": serializer.errors},
            )
        name = serializer.validated_data["name"]
        director = Directors.objects.create(name=name)
        director.save()
        return Response(
            status=status.HTTP_201_CREATED,
            data={
                "message": "Director created",
                "director": DirectorDetailSerializers(name).data,
            },
        )


@api_view(["GET"])
def director_detail_view(request, id):
    directors = Directors.objects.get(id=id)
    data = DirectorDetailSerializers(directors, many=False).data
    return Response(data=data)


@api_view(["GET", "POST"])
def review_list_view(request):
    if request.method == "GET":
        review = Review.objects.all()
        data = ReviewSerializers(review, many=True).data
        return Response(data=data)
    else:
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_406_NOT_ACCEPTABLE,
                data={"errors": serializer.errors},
            )
        text = serializer.validated_data["text"]
        stars = serializer.validated_data["stars"]
        movie_id = serializer.validated_data["movie_id"]
        review = Review.objects.create(text=text, stars=stars, movie_id=movie_id)
        review.save()
        return Response(
            status=status.HTTP_201_CREATED,
            data={
                "message": "Review created",
                "review": ReviewDetailSerializers(review).data,
            },
        )


@api_view(["GET", "PUT", "DELETE"])
def review_detail_view(request, id):
    review = Review.objects.get(id=id)
    if request.method == "GET":
        data = ReviewDetailSerializers(review, many=False).data
        return Response(data=data)
    elif request.method == "DELETE":
        review.delete()
        return Response(data={"message": "Review removed"})
    else:
        serializer = MovieValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_406_NOT_ACCEPTABLE,
                data={"errors": serializer.errors},
            )
        review.text = serializer.validated_data["text"]
        review.stars = serializer.validated_data["stars"]
        review.movie_id = serializer.validated_data["movie_id"]
        review.save()
        return Response(data=ReviewDetailSerializers(review).data)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def movie_list_view(request):
    print(request.user1)
    if request.method == "GET":
        movies = Movie.objects.all()
        data = MovieSerailizer(movies, many=True).data
        return Response(data=data)
    else:
        serializer = MovieValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_406_NOT_ACCEPTABLE,
                data={"errors": serializer.errors},
            )
        title = serializer.validated_data["title"]
        description = serializer.validated_data["description"]
        duration = serializer.validated_data["duration"]
        genre_id = serializer.validated_data["genre_id"]
        tags = serializer.validated_data["tags"]
        movies = Movie.objects.create(
            title=title, description=description, duration=duration, genre_id=genre_id
        )
        movies.tags.set(tags)
        movies.save()
        return Response(
            status=status.HTTP_201_CREATED,
            data={
                "message": "Movie created",
                "movies": MovieDetailSerializers(movies).data,
            },
        )


@api_view(["GET", "PUT", "DELETE"])
def movie_detail_view(request, id):
    try:
        movies = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(
            status=status.HTTP_404_NOT_FOUND, data={"error": "no such movie!"}
        )
    # Получить все отзывы фильтр
    # reviews = movies.reviews.all()
    # Отзывы по фильму ручной филтр
    # reviews = Review.objects.filter(movies=movies)
    movies = Movie.objects.get(id=id)
    if request.method == "GET":
        data = MovieDetailSerializers(movies, many=False).data
        return Response(data=data)
    elif request.method == "DELETE":
        movies.delete()
        return Response(data={"message": "Movie removed"})
    serializer = MovieValidateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            status=status.HTTP_406_NOT_ACCEPTABLE, data={"errors": serializer.errors}
        )
    else:
        movies.title = serializer.validated_data["title"]
        movies.description = serializer.validated_data["description"]
        movies.duration = serializer.validated_data["duration"]
        movies.genre_id = serializer.validated_data["genre_id"]
        movies.tags.set(serializer.validated_data["tags"])
        movies.save()
        return Response(data=MovieDetailSerializers(movies).data)


@api_view(["GET"])
def static_data_view(request):
    dict_ = {"key": "good"}
    return Response(data=dict_)
