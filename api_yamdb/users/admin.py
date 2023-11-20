from django.contrib import admin

from users.models import CustomUser
from api_yamdb.settings import PAGE_SIZE


admin.site.register(CustomUser)


class UserAdmin(admin.ModelAdmin):
    """Класс настройки раздела пользователей."""
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role',
    )
    empty_value_display = 'значение отсутствует'
    list_editable = ('role',)
    list_filter = ('username',)
    list_per_page = PAGE_SIZE
    search_fields = ('username', 'role')
