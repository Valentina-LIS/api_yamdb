from django.contrib import admin

from reviews.models import Genre, Category, Title

admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Title)
