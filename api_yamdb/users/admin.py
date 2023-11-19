from django.contrib import admin

from users.models import CustomUser
from reviews.models import Genre, Category, Title

admin.site.register(CustomUser)
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Title)
