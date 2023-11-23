from rest_framework.mixins import (
    ListModelMixin, CreateModelMixin, DestroyModelMixin
)
from rest_framework.viewsets import GenericViewSet


class ListCreateDestroyMixin(ListModelMixin,
                             CreateModelMixin,
                             DestroyModelMixin,
                             GenericViewSet):
    """Набор миксинов для жанров и категорий."""
