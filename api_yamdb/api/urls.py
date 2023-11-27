from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    CategoryViewSet,
    CommentsViewSet,
    CustomUserViewSet,
    GenreViewSet,
    ReviewsViewSet,
    SignupView,
    TitleViewSet,
    TokenView
)

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(r'genres', GenreViewSet, basename='genres')
router_v1.register(r'users', CustomUserViewSet, basename='users')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewsViewSet, basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments',
)

urlpatterns = [
    path('v1/auth/token/', TokenView.as_view(), name='get_token'),
    path('v1/auth/signup/', SignupView.as_view(), name='signup'),
    path('v1/', include(router_v1.urls)),
]
