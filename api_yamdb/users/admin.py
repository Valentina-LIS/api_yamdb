from django.conf import settings
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin

from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """Класс настройки раздела пользователей."""

    list_display = ('username', 'email', 'first_name',
                    'last_name', 'bio', 'role',)
    empty_value_display = 'значение отсутствует'
    list_editable = ('role',)
    list_filter = ('username',)
    list_per_page = settings.PAGE_SIZE
    search_fields = ('username', 'role')
