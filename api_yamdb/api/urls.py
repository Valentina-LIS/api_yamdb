from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (TitleViewSet, GenreViewSet, CategoryViewSet)

router_v1 = DefaultRouter()
router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(r'genres', GenreViewSet, basename='genres')

urlpatterns = [
    path('v1/', include(router_v1.urls),),
]
