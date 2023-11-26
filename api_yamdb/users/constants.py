# Roles
ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'

# constants
FIELD_DEFAULT_LEN = 150
"""Длина полей по умолчанию для модели CustomUser."""

EMAIL_FIELD_LEN = 254
"""Длина поля электронной почты."""

CONFIRM_CODE_SIZE = 6
"""Длина кода подтверждения."""

USERNAME_REGEX = r'^[\w.@+-]+$'
"""Валидатор имени пользователя."""

PROHIBITED_USERNAMES = ('me', 'admin')
"""Имена пользователей запрещенные к регистрации."""
