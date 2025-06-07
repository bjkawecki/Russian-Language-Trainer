from django.urls import path

from apps.decks.views import DeckDetail

urlpatterns = [
    path("courses/deck/<slug:slug>/", DeckDetail.as_view(), name="deck_details"),
]
