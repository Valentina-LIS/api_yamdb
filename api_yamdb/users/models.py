from django.contrib.auth.models import AbstractUser
from django.db import models

from users.constants import (
    ADMIN, EMAIL_FIELD_LEN, FIELD_DEFAULT_LEN, MODERATOR, USER
)


class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN_ROLE = (ADMIN, 'Администратор')
        MODERATOR_ROLE = (MODERATOR, 'Модератор')
        USER_ROLE = (USER, 'Пользователь')

    first_name = models.CharField(
        'Имя',
        max_length=FIELD_DEFAULT_LEN,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=FIELD_DEFAULT_LEN,
        blank=True
    )
    email = models.EmailField(
        'E-mail',
        unique=True,
        max_length=EMAIL_FIELD_LEN
    )
    role = models.CharField(
        'Роль',
        default=USER,
        max_length=FIELD_DEFAULT_LEN,
        choices=Roles.choices
    )
    bio = models.TextField(
        'О себе',
        blank=True
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=FIELD_DEFAULT_LEN,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return (
            self.role == self.Roles.ADMIN_ROLE
            or (self.is_staff and self.is_superuser)
        )

    @property
    def is_moderator(self):
        return self.role == self.Roles.MODERATOR_ROLE

    @property
    def is_user(self):
        return self.role == self.Roles.USER_ROLE
