from django.utils import timezone
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        model = Category
        fields = ('name', 'slug', )


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        model = Genre
        fields = ('name', 'slug', )


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
