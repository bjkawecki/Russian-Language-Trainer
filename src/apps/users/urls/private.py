from django.urls import path

from apps.users.views import faq

urlpatterns = [
    path("profile/help/", faq.Faq.as_view(), name="help"),
]
