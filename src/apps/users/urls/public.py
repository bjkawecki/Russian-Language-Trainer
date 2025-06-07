from django.urls import path

from apps.users.views.public import (
    CancellationView,
    ImpressumView,
    LandingPage,
    PrivacyView,
    TermsView,
)

urlpatterns = [
    path("", LandingPage.as_view(), name="landingpage"),
    path("impressum/", ImpressumView.as_view(), name="impressum"),
    path("agb/", TermsView.as_view(), name="terms"),
    path("widerrufsbelehrung/", CancellationView.as_view(), name="cancellation"),
    path("datenschutzerklaerung/", PrivacyView.as_view(), name="privacy"),
]
