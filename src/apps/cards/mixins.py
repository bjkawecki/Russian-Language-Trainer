from django.db.models import Q
from django.db.models.functions import Lower

from apps.words.models.word import Word


class CardListMixin:
    def build_filters(self, user, search_text, wordclass_filter) -> Q:
        filters = Q(user=user, word__course__user=user)
        if search_text:
            filters &= Q(word__lemma__icontains=search_text) | Q(
                word__translation__name__icontains=search_text
            )
        if wordclass_filter:
            filters &= Q(word__wordclass__in=wordclass_filter)
        return filters

    def apply_ordering(self, queryset, order):
        order_field = Lower("word__lemma")
        if order == "desc":
            return queryset.order_by(order_field.desc())
        return queryset.order_by(order_field)

    def get_wordclass_choices(self):
        return {value: display for value, display in Word.WordClass.choices}
