from rest_framework import filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from reviews.models import Category, Genre, Title
from api.filters import TitleFilter
from api.serializers import (CategorySerializer, CommentsSerializer,
                             GenreSerializer, ReviewsSerializer,
                             TitleSerializer, TitleCreateSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    """Произведения."""
    serializer_class = TitleSerializer
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('name')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        """Определяет какой сериализатор будет использоваться
        для разных типов запроса."""
        if self.request.method == 'GET':
            return TitleSerializer
        return TitleCreateSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """Категории."""
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(viewsets.ModelViewSet):
    """Жанры."""
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class ReviewsViewSet(viewsets.ModelViewSet):
    """Отзывы."""
    serializer_class = ReviewsSerializer

    def get_queryset(self):

        pass

    def perform_create(self, serializer):

        pass


class CommentsViewSet(viewsets.ModelViewSet):
    """Комментарии."""
    serializer_class = CommentsSerializer

    def get_queryset(self):

        pass

    def perform_create(self, serializer):

        pass
