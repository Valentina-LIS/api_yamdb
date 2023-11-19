from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CategoryViewSet, CommentsViewSet,
                       GenreViewSet, ReviewsViewSet, TitleViewSet)
from users.views import CustomUserViewSet

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
    path('v1/', include('users.urls')),
    path('v1/', include(router_v1.urls)),
]
