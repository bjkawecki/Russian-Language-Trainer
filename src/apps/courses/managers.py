from django.db import models
from django.db.models import Count, Q

from apps.cards.enums import CardState


class CourseManager(models.Manager):
    def count_cards_and_decks(self, user=None):
        user_filter = Q()
        if user:
            user_filter &= Q(word__card__user=user)
        return self.annotate(
            all_decks=Count("deck", filter=Q(user_filter), distinct=True),
            all_cards=Count("word", filter=Q(user_filter), distinct=True),
            initial_cards=Count(
                "word",
                filter=Q(user_filter, word__card__state=CardState.INITIAL),
                distinct=True,
            ),
            in_progress_cards=Count(
                "word",
                filter=Q(user_filter, word__card__state=CardState.IN_PROGRESS),
                distinct=True,
            ),
            mastered_cards=Count(
                "word",
                filter=Q(user_filter, word__card__state=CardState.MASTERED),
                distinct=True,
            ),
        )
