from django.core.validators import RegexValidator
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers, status, response, validators

from reviews.models import Category, Comment, Genre, Review, Title
from users.constants import (
    FIELD_DEFAULT_LEN, PROHIBITED_USERNAMES, USERNAME_REGEX
)
from users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=FIELD_DEFAULT_LEN,
        validators=[
            RegexValidator(
                regex=USERNAME_REGEX,
                message='Доступны только буквы, цифры и нижнее подчеркивания'
            ),
            validators.UniqueValidator(queryset=CustomUser.objects.all())
        ]
    )

    class Meta:
        model = CustomUser
        fields = (
            'first_name', 'last_name', 'email', 'username', 'role', 'bio'
        )


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=FIELD_DEFAULT_LEN)
    confirmation_code = serializers.CharField(max_length=FIELD_DEFAULT_LEN)

    def validate(self, attrs):
        username = attrs.get('username')
        confirmation_code = attrs.get('confirmation_code')

        if not username:
            raise serializers.ValidationError('Поле "username" обязательное')

        try:
            user = get_object_or_404(CustomUser, username=username)
        except CustomUser.DoesNotExist:
            return response.Response(
                f'Пользователь {username} не существует',
                status=status.HTTP_404_NOT_FOUND
            )

        if user.confirmation_code != confirmation_code:
            raise serializers.ValidationError(
                'Недействительный код подтверждения'
            )

        return attrs


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'username')

    def validate(self, attrs):
        email = attrs.get('email')
        username = attrs.get('username')

        if username.lower() in PROHIBITED_USERNAMES:
            raise serializers.ValidationError(
                f'"{username}" нельзя использовать'
            )

        if CustomUser.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError('E-mail уже существует')

        if CustomUser.objects.filter(username__iexact=username).exists():
            raise serializers.ValidationError(f'"{username}" уже существует')

        return attrs


class CustomUserMeSerializer(CustomUserSerializer):
    role = serializers.CharField(read_only=True)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        model = Category
        fields = ('name', 'slug',)


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class TitleSerializer(serializers.ModelSerializer):
    """Сериалайзер для получения произведений."""

    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        read_only_fields = ('id', 'rating',)


class TitleCreateSerializer(serializers.ModelSerializer):
    """Сериалайзер для создания произведений."""

    category = serializers.SlugRelatedField(read_only=False,
                                            slug_field='slug',
                                            queryset=Category.objects.all())
    genre = serializers.SlugRelatedField(many=True,
                                         read_only=False,
                                         slug_field='slug',
                                         queryset=Genre.objects.all())

    class Meta:
        model = Title
        fields = ('id', 'name', 'year',
                  'description', 'genre', 'category')
        read_only_fields = ('id',)
        lookup_field = 'genre__slug'

    def validate_year(self, value):
        """
        Проверка, что значение поля year не отрицательное
        и не больше текущего года.
        """
        if value > timezone.now().year:
            raise serializers.ValidationError(
                detail={
                    'year': 'Значение года не может быть больше текущего'
                }
            )
        if value < 0:
            raise serializers.ValidationError(
                detail={
                    'year': 'Значение года не может быть отрицательным'
                }
            )
        return value


class ReviewsSerializer(serializers.ModelSerializer):
    """Сериалайзер для отзывов."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('id', 'title', 'author', 'pub_date')

    def validate_score(self, score):
        """
        Проверка рейтинга, что в диапозоне от 0 до 10.
        """
        if not (0 < score <= 10):
            raise serializers.ValidationError(
                'Рейтинг должен быть в интервале от 1 до 10.'
            )
        return score

    def validate(self, data):
        """
        Проверка на уникальность.
        1 отзыв от 1 автора для 1 произведения.
        """
        request = self.context.get('request')
        title = self.context.get('view').kwargs.get('title_id')
        review_exists = Review.objects.filter(title=title,
                                              author=request.user).exists()
        is_post_request = request.method == 'POST'
        if review_exists and is_post_request:
            raise serializers.ValidationError(
                'Можно оставить только один отзыв!'
            )
        return data


class CommentsSerializer(serializers.ModelSerializer):
    """Сериалайзер для комментариев."""
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        model = Comment
        fields = ('id', 'review', 'text', 'author', 'pub_date')
        read_only_fields = ('review',)
