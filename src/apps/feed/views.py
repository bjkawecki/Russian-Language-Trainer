from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import StreamingHttpResponse
from django.utils.functional import cached_property
from django.views.generic import ListView, View

from apps.announcements.mixins import AnnouncementsMixin
from apps.decks.models import Deck
from apps.feed.mixins import FeedMixin, FeedSSEMixin
from apps.shared.mixins import CalendarMixin, WidgetsMixin
from apps.users.models import User


class FeedView(
    LoginRequiredMixin,
    AnnouncementsMixin,
    CalendarMixin,
    WidgetsMixin,
    FeedMixin,
    ListView,
):
    model = Deck
    context_object_name = "user_decks"

    def get_queryset(self):
        user = self.request.user
        if user:
            deck_list = self.get_feed_queryset(user)
            return deck_list

    @cached_property
    def user(self):
        user: User = self.request.user
        return user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_calendar_context(self.user))
        context.update(self.get_daily_proverb(self.user))
        context.update(self.get_review_context(self.user))
        context.update(self.get_feed_context(self.user))
        return context


class NewDecksView(LoginRequiredMixin, FeedMixin, ListView):
    model = Deck
    template_name = "feed-new/feed-new.html"
    context_object_name = "new_decks"
    paginate_by = 15

    @cached_property
    def user(self):
        user: User = self.request.user
        return user

    def get_template_names(self):
        # Wenn die Anfrage von HTMX kommt, rendere nur die Teilansicht
        if self.request.headers.get("HX-Request"):
            action = self.request.GET.get("action")
            if action == "next":
                return ["feed-new/components/decks.html"]
            return ["feed-new/feed-new.html"]

    def get_queryset(self, **kwargs):
        selected_course = self.request.GET.get("selected_course", "").strip()
        return self.get_newdecks(self.user, selected_course)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["selected_course"] = self.request.GET.get("selected_course", "").strip()
        context.update(self.get_newdecks_context(self.user))
        return context


class DueDecksView(LoginRequiredMixin, FeedMixin, ListView):
    model = Deck
    template_name = "feed-due/feed-due.html"
    context_object_name = "due_decks"
    paginate_by = 10

    @cached_property
    def user(self):
        user: User = self.request.user
        return user

    def get_queryset(self, **kwargs):
        return self.get_duedecks(self.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_duedecks_context(self.user))
        return context


class FeedSSE(FeedSSEMixin, View):
    def get(self, *args, **kwargs):
        user = self.request.user
        response = StreamingHttpResponse(self.send_due_decks(user))
        response["Content-Type"] = "text/event-stream"
        return response
