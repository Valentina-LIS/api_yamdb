from django.utils import timezone
from rest_framework import serializers

from reviews.models import Category, Genre, Title


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
