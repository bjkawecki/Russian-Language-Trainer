from django.urls import path

from apps.users.views.public import (
    LoginPage,
    SignupPage,
    logout_user,
    CustomPasswordResetView,
)

urlpatterns = [
    path("logout/", logout_user, name="logout"),
    path("signup/", SignupPage.as_view(), name="signup"),
    path("signin/", LoginPage.as_view(), name="signin"),
    path(
        "account-reset-password/",
        CustomPasswordResetView.as_view(),
        name="reset_password",
    ),
]
