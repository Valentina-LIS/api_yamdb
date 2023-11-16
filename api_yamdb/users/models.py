from django.contrib.auth.models import AbstractUser
from django.db import models

from users.constants import ADMIN, FIELD_DEFAULT_LEN, MODERATOR, USER


class CustomUser(AbstractUser):
    ADMIN_ROLE = ADMIN
    MODERATOR_ROLE = MODERATOR
    USER_ROLE = USER
    CHOICES_ROLE = (
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь'),
    )
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
        max_length=FIELD_DEFAULT_LEN
    )
    role = models.CharField(
        'Роль',
        default=USER,
        max_length=FIELD_DEFAULT_LEN,
        choices=CHOICES_ROLE
    )
    bio = models.TextField(
        'О себе',
        blank=True
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=FIELD_DEFAULT_LEN,
        null=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return (
            self.role == self.ADMIN_ROLE
            or (self.is_staff and self.is_superuser)
        )

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR_ROLE

    @property
    def is_user(self):
        return self.role == self.USER_ROLE

    def __str__(self):
        return self.username
