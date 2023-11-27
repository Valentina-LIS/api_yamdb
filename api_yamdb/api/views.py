from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import (
    filters,
    permissions,
    response,
    status,
    viewsets
)
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView

from api.core import send_confirmation_code
from api.filters import TitleFilter
from api.mixins import ListCreateDestroyMixin
from api.permissions import (
    IsAdmin,
    IsAdminOrReadOnly,
    IsAuthorModeratorAdminOrReadOnly
)
from api.serializers import (
    CategorySerializer,
    CommentsSerializer,
    CustomUserSerializer,
    CustomUserMeSerializer,
    GenreSerializer,
    ReviewsSerializer,
    SignupSerializer,
    TitleSerializer,
    TitleCreateSerializer,
    TokenSerializer
)
from reviews.models import Category, Genre, Title, Review
from users.models import CustomUser


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdmin)
    search_fields = ('username',)
    filter_backends = (filters.SearchFilter,)
    http_method_names = ('get', 'post', 'patch', 'delete')
    lookup_field = 'username'

    @action(detail=False,
            methods=('GET', 'PATCH'),
            permission_classes=(permissions.IsAuthenticated,))
    def me(self, request):
        if request.method == 'GET':
            serializer = CustomUserSerializer(request.user)
            return response.Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        serializer = CustomUserMeSerializer(
            request.user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class TokenView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            user = get_object_or_404(CustomUser, username=username)
            token = AccessToken.for_user(user)
            return response.Response(token, status=status.HTTP_200_OK)
        return response.Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class SignupView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        username = request.data.get('username')

        if CustomUser.objects.filter(email=email, username=username).exists():
            send_confirmation_code(request)
            return response.Response(request.data, status=status.HTTP_200_OK)

        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        send_confirmation_code(request)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class TitleViewSet(viewsets.ModelViewSet):
    """Произведения."""
    serializer_class = TitleSerializer
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('name').select_related('category').prefetch_related('genre')
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_serializer_class(self):
        """Определяет какой сериализатор будет использоваться
        для разных типов запроса."""
        if self.request.method == 'GET':
            return TitleSerializer
        return TitleCreateSerializer


class CategoryViewSet(ListCreateDestroyMixin):
    """Категории."""
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyMixin):
    """Жанры."""
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class ReviewsViewSet(viewsets.ModelViewSet):
    """Отзывы."""
    serializer_class = ReviewsSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all().select_related('author')

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    """Комментарии."""
    serializer_class = CommentsSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.all().select_related('author')

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, review=review)
