import random
import string

from django.core.mail import send_mail
from rest_framework.generics import get_object_or_404

from users.constants import CONFIRM_CODE_SIZE, NO_REPLY_MAIL
from users.models import CustomUser


def send_confirmation_code(request):
    user = get_object_or_404(
        CustomUser, username=request.data.get('username')
    )
    token = random.choices(
        string.ascii_letters + string.digits,
        k=CONFIRM_CODE_SIZE
    )
    user.confirmation_code = ''.join(token)
    user.save()
    send_mail(
        'Код подтвержения',
        f'Ваш код {user.confirmation_code} никому не сообщайте.',
        NO_REPLY_MAIL,
        [request.data.get('email')],
        fail_silently=False,
    )
