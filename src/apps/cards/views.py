import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Aggregate, CharField, Value
from django.db.models.functions import Coalesce
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.views.generic import DetailView, ListView

from apps.cards.enums import CardState
from apps.cards.mixins import CardListMixin
from apps.cards.models import Card

logger = logging.getLogger("django")


class StringAgg(Aggregate):
    function = "STRING_AGG"
    template = "%(function)s(%(expressions)s, ', ')"
    output_field = CharField()


class CardList(LoginRequiredMixin, CardListMixin, StringAgg, ListView):
    model = Card
    template_name = "card-list/card-list.html"
    context_object_name = "usercards"
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        """
        Generate the queryset for Card objects, with filters and sorting based on request parameters.
        """
        user = self.request.user
        order = self.request.GET.get("order", None)
        search_text = self.request.GET.get("search", "").strip()
        word_class_filter = self.request.GET.getlist("filter", [])

        filters = self.build_filters(user, search_text, word_class_filter)

        queryset = (
            Card.objects.only(
                "id",
                "word__wordclass",
                "word__lemma_accent",
                "word__slug",
                "user__id",
                "state",
            )
            .filter(filters)
            .prefetch_related("word__translation_set")
            .annotate(
                translations_string=Coalesce(
                    StringAgg("word__translation__name"), Value("")
                )
            )
            .distinct()
        )
        return self.apply_ordering(queryset, order)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_text = self.request.GET.get("search")
        word_class_filter = self.request.GET.getlist("filter")
        word_class_filter = list(map(str, word_class_filter))
        order = self.request.GET.get("order", None)
        if not order or order == "asc":
            context["order"] = "desc"
        else:
            context["order"] = "asc"

        context["searchtext"] = search_text
        context["word_class_filter"] = word_class_filter
        context["wordclasses"] = self.get_wordclass_choices()

        return context


class CardDetails(LoginRequiredMixin, DetailView):
    model = Card
    template_name = "card-detail/card-detail.html"
    context_object_name = "card"

    def get_object(self):
        slug = self.kwargs["slug"]
        user = self.request.user
        self.card = Card.objects.select_related("word").get(word__slug=slug, user=user)
        return self.card

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["audio"] = self.card.word.audio or None
        context["translation"] = self.card.get_joined_translation() or []
        return context


def reset_usercard(request, pk):
    user = request.user
    usercard = Card.objects.filter(id=pk, user=user)
    usercard.update(
        ease=170, due_date=timezone.now(), state=CardState.INITIAL, interval=0
    )
    messages.success(
        request,
        (f"Ihr Fortschritt der Karte {usercard[0].word.lemma} wurde zurückgesetzt."),
    )
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
