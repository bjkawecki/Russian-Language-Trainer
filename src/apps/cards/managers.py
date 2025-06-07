from django.db import models
from django.db.models import Count, Q
from django.utils import timezone

from apps.cards.enums import CardState


class CardManager(models.Manager):
    def count_by_state(self, user, due_deck_list=None):
        if due_deck_list is None:
            due_deck_list = []

        now = timezone.now()
        # 1. Basis-QuerySet: Nur Karten dieses Users
        base_qs = self.filter(user=user)
        # 2. Aggregate alles auf EINMAL
        counts = base_qs.aggregate(
            all_cards=Count("pk", distinct=True),
            due_cards=Count(
                "pk",
                filter=Q(due_date__lt=now, word__deck__in=due_deck_list),
                distinct=True,
            ),
            initial_cards=Count("pk", filter=Q(state=CardState.INITIAL), distinct=True),
            in_progress_cards=Count(
                "pk",
                filter=Q(state__in=[CardState.IN_PROGRESS, CardState.REVIEW]),
                distinct=True,
            ),
            mastered_cards=Count(
                "pk", filter=Q(state=CardState.MASTERED), distinct=True
            ),
        )
        return counts

    def get_due_cards(self, user):
        now = timezone.now()
        return (
            self.filter(due_date__gte=now, user=user)
            .exclude(state=CardState.INITIAL)
            .order_by("due_date")
        )
