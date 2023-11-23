from django.urls import path

from users.views import SignupView, TokenView

urlpatterns = [
    path('auth/token/', TokenView.as_view(), name='get_token'),
    path('auth/signup/', SignupView.as_view(), name='signup'),
]
