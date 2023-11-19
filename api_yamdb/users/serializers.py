from django.core.validators import RegexValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status, response, validators

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
    email = serializers.EmailField(max_length=FIELD_DEFAULT_LEN)

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


class CustomUserMeSerializer(CustomUserSerializer):
    role = serializers.CharField(read_only=True)
