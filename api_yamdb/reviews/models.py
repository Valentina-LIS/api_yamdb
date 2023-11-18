from django.db import models

from django.core.validators import RegexValidator

LENGTH_TEXT = 15


class Genre(models.Model):
    """Модель жанров."""
    name = models.CharField(
        verbose_name='Название жанра',
        max_length=256,
        db_index=True
    )
    slug = models.SlugField(
        verbose_name='Слаг жанра',
        max_length=50,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message='Слаг жанра содержит недопустимый символ'
        )]
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:LENGTH_TEXT]


class Category(models.Model):
    """Модель категорий."""
    name = models.CharField(
        verbose_name='Название категории',
        max_length=100,
        db_index=True
    )
    slug = models.SlugField(
        verbose_name='Слаг категории',
        max_length=50,
        unique=True,
        db_index=True,
        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message='Слаг категории содержит недопустимый символ'
        )]
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:LENGTH_TEXT]


class Title(models.Model):
    """Модель произведений."""
    name = models.CharField(
        verbose_name='Название произведения',
        max_length=256,
        db_index=True
    )
    year = models.PositiveIntegerField(
        verbose_name='Год выпуска',
        db_index=True,
    )
    description = models.TextField(
        verbose_name='Описание',
        max_length=256,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанр',
        related_name='titles'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='category',
        verbose_name='Категория',
        null=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:LENGTH_TEXT]


class GenreTitle(models.Model):
    """Вспомогательная модель, связывает жанры и произведения."""
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Соответствие жанра и произведения'
        verbose_name_plural = 'Таблица соответствия жанров и произведений'

    def __str__(self):
        return f'{self.title} принадлежит жанр(у/ам) {self.genre}'
