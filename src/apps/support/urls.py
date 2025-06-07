from django.urls import path

from apps.support.views import UserMessageView

urlpatterns = [
    path("profile/contact-form/", UserMessageView.as_view(), name="contact_form"),
]
