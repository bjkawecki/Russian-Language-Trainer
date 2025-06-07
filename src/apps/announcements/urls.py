from django.urls import path

from apps.announcements.views import Announcements

urlpatterns = [
    path("announcements/", Announcements.as_view(), name="announcement_list"),
]
