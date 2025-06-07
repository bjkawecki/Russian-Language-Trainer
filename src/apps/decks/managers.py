from django.db import models
from django.db.models import Count, Q
from django.utils import timezone

from apps.cards.enums import CardState


class DeckManager(models.Manager):
    def count_cards(self, user):
        now = timezone.now()
        user_filter = Q(word__card__user=user)
        return self.annotate(
            all_cards=Count("word", filter=Q(user_filter)),
            due_cards=Count(
                "word", filter=Q(user_filter, word__card__due_date__lte=now)
            ),
            initial_cards=Count(
                "word", filter=Q(user_filter, word__card__state=CardState.INITIAL)
            ),
            in_progress_cards=Count(
                "word", filter=Q(user_filter, word__card__state=CardState.IN_PROGRESS)
            ),
            mastered_cards=Count(
                "word", filter=Q(user_filter, word__card__state=CardState.MASTERED)
            ),
        )

    def count_due_cards(self, user):
        now = timezone.now()
        user_filter = Q(word__card__user=user)
        due_filter = Q(word__card__due_date__lt=now)

        return self.annotate(
            all_cards=Count("word", filter=user_filter, distinct=True),
            due_cards=Count("word", filter=user_filter & due_filter, distinct=True),
            initial_cards=Count(
                "word",
                filter=user_filter & Q(word__card__state=CardState.INITIAL),
                distinct=True,
            ),
            due_in_progress_cards=Count(
                "word",
                filter=user_filter
                & due_filter
                & Q(word__card__state=CardState.IN_PROGRESS),
                distinct=True,
            ),
            due_mastered_cards=Count(
                "word",
                filter=user_filter
                & due_filter
                & Q(word__card__state=CardState.MASTERED),
                distinct=True,
            ),
        )
