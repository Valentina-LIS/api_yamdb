from django.urls import path

from .views import SignupView, TokenView

urlpatterns = [
    path('auth/token/', TokenView.as_view()),
    path('auth/signup/', SignupView.as_view()),
]
