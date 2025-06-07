from django.urls import path

from apps.cards.views import CardDetails, CardList, reset_usercard

urlpatterns = [
    path("cards/", CardList.as_view(), name="card_list"),
    path("cards/<slug:slug>/", CardDetails.as_view(), name="card_details"),
    path("cards/<str:pk>/reset/", reset_usercard, name="card_details_reset"),
]
