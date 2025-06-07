import json
import time

from django.core.serializers.json import DjangoJSONEncoder
from django.db import connection
from django.db.models import F, Max, Q

from apps.cards.models import Card
from apps.courses.models import Course
from apps.decks.models import Deck


class UserDecksMixin:
    def _get_userdecks(self, user):
        return (
            Deck.objects.count_due_cards(user)
            .filter(user=user, course__in=user.course_set.all())
            .alias(latest_usercard=Max("word__card__due_date"))
        )


class FeedMixin(UserDecksMixin):
    def get_newdecks(self, user, selected_course=None):
        query = self._get_userdecks(user).filter(all_cards=F("initial_cards"))
        if not selected_course:
            return query.order_by("course__name")
        return query.filter(course__name=selected_course).order_by("course__name")

    def get_duedecks(self, user):
        return (
            self._get_userdecks(user)
            .order_by("latest_usercard")
            .exclude(Q(all_cards=F("initial_cards")) | Q(due_cards=0))
        )

    def get_newdecks_context(self, user):
        context = {}
        user_decks = self._get_userdecks(user)
        due_deck_list = list(filter(lambda deck: deck.is_not_new_deck(), user_decks))
        context["cards_status"] = Card.objects.count_by_state(user, due_deck_list)
        context["user_courses"] = (
            Course.objects.filter(user=user).values("name").order_by("name")
        )
        return context

    def get_duedecks_context(self, user):
        context = {}
        user_decks = self._get_userdecks(user)
        due_deck_list = list(filter(lambda deck: deck.is_not_new_deck(), user_decks))
        context["due_deck_list"] = due_deck_list
        context["cards_status"] = Card.objects.count_by_state(user, due_deck_list)
        return context

    def get_feed_queryset(self, user):
        due_decks = self._get_userdecks(user).exclude(all_cards=F("initial_cards"))
        if not due_decks:
            new_deck_list = self._get_userdecks(user).filter(
                all_cards=F("initial_cards")
            )
            return new_deck_list
        return due_decks

    def get_feed_context(self, user):
        """Handle user cards and categorize decks."""
        context = {}
        if not user.has_course():
            self.template_name = "feed/no-subscription.html"
            return context
        user_decks = self._get_userdecks(user)
        due_deck_list = list(filter(lambda deck: deck.is_not_new_deck(), user_decks))
        new_deck_list = list(filter(lambda deck: deck.is_new_deck(), user_decks))
        if new_deck_list:
            context["has_new_decks"] = True
        if due_deck_list:
            context["has_due_decks"] = True
        context["cards_status"] = Card.objects.count_by_state(
            user=user, due_deck_list=due_deck_list
        )
        self.template_name = "feed/feed.html"
        return context


class FeedSSEMixin(UserDecksMixin):
    def _get_duedecks_values(self, user):
        return (
            self._get_userdecks(user)
            .exclude(Q(all_cards=F("initial_cards")) | Q(due_cards=0))
            .values(
                "id",
                "name",
                "due_cards",
                "initial_cards",
                "due_in_progress_cards",
                "due_mastered_cards",
                "course__name",
            )
        )

    def send_due_decks(self, user):
        initial_data = ""
        sleep_interval = 10
        while True:
            decks = list(self._get_duedecks_values(user))
            connection.close()
            data = json.dumps(decks, cls=DjangoJSONEncoder)
            if data != initial_data:
                yield f"\ndata: {data}\n\n"
                initial_data = data
            time.sleep(sleep_interval)


class StripeMixin:
    def get_stripe_subscription_context(self, user):
        from apps.users.services.stripe import get_user_subscription

        user_subscription = get_user_subscription(user)
        if user_subscription and user_subscription.status == "active":
            pass
        else:
            self.template_name = "feed/subscription-not-active.html"
