from django.urls import path

from apps.feed.views import DueDecksView, FeedSSE, FeedView, NewDecksView

urlpatterns = [
    path("feed/", FeedView.as_view(), name="feed"),
    path("feed/update/", FeedSSE.as_view(), name="feed_sse"),
    path("feed/due-decks/", DueDecksView.as_view(), name="due_decks"),
    path("feed/new-decks/", NewDecksView.as_view(), name="new_decks"),
]
