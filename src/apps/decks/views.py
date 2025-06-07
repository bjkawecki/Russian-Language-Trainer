from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, Paginator
from django.db.models import Aggregate, CharField, Value
from django.db.models.functions import Coalesce
from django.shortcuts import render
from django.views.generic import DetailView

from apps.cards.models import Card
from apps.decks.models import Deck


class StringAgg(Aggregate):
    function = "STRING_AGG"
    template = "%(function)s(%(expressions)s, ', ')"
    output_field = CharField()


class DeckDetail(LoginRequiredMixin, DetailView):
    model = Deck
    template_name = "deck-detail/deck-detail.html"

    def get_object(self):
        user = self.request.user
        slug = self.kwargs["slug"]
        return Deck.objects.count_cards(user).get(slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        page_number = self.request.GET.get("page", 1)
        deck = self.get_object()
        cards = (
            Card.objects.select_related("word")
            .prefetch_related("word__translation_set")
            .filter(word__deck=deck, user=user)
            .annotate(
                translations_string=Coalesce(
                    StringAgg("word__translation__name"), Value("")
                )
            )
        )
        paginator = Paginator(cards, 10)

        try:
            page_obj = paginator.page(page_number)
        except EmptyPage:
            page_obj = None

        context["page_obj"] = page_obj
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.htmx:
            return render(self.request, "deck-detail/partials/card-list.html", context)
        return super().render_to_response(context, **response_kwargs)
