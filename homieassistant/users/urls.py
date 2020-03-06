from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

app_name = "users"


urlpatterns = [
    path("register/", views.RegistrationView.as_view(), name="register"),
    path("me/", views.UserMeView.as_view(), name="user-me"),
    path(
        "change-password/", views.ChangePasswordView.as_view(), name="change-password"
    ),
    path("reset-password/", views.RestorePasswordView.as_view(), name="reset-password"),
    path(
        "reset-password-confirm/<uuid:user_id>/",
        views.RestorePasswordConfirmView.as_view(),
        name="reset-password-confirm",
    ),
    path("token/", obtain_auth_token, name="token"),
]
