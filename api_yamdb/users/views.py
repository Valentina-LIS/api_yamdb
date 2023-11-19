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

from users.core import send_confirmation_code
from users.models import CustomUser
from users.permissions import IsAdmin
from users.serializers import (
    CustomUserSerializer,
    CustomUserMeSerializer,
    SignupSerializer,
    TokenSerializer
)


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdmin)
    search_fields = ('username',)
    filter_backends = (filters.SearchFilter,)
    http_method_names = ('get', 'post', 'patch', 'put', 'delete')
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
        email = request.get('email')
        username = request.get('username')

        if CustomUser.objects.filter(email=email, username=username).exists():
            send_confirmation_code(request)
            return response.Response(request.data, status=status.HTTP_200_OK)

        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        send_confirmation_code(request)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
