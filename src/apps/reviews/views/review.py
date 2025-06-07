import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.http import Http404
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import TemplateView

from apps.cards.models import Card
from apps.decks.models import Deck
from apps.reviews.forms import ReviewForm
from apps.reviews.mixins.review import NewReviewMixin, ReviewMixin, TurboReviewMixin

logger = logging.getLogger("debug")


class ReviewBaseView(LoginRequiredMixin, ReviewMixin, NewReviewMixin, TemplateView):
    def is_card_due(self, active_card):
        """Überprüft, ob die Karte fällig ist."""
        return active_card["due_date"] < timezone.now()

    def render_empty_page(self, context):
        """Zeigt die leere Seite an, wenn die Karte noch nicht fällig ist."""
        return render(self.request, "review/form_empty.html", context)

    def render_invalid_form(self, context):
        """Zeigt das Formular bei Fehlern an."""
        return render(self.request, "review/form_invalid.html", context)

    def _build_context_for_next_page(self, context, active_card, updated_data):
        context.update(
            {
                "audio": active_card["word__audio"],
                "interval": self.humanize_interval(interval=updated_data["interval"]),
                "active_card": active_card["word__lemma_accent"],
            }
        )
        return context

    def _update_usercard_and_review(
        self, card_id, previous_state, updated_data, user_id
    ):
        self.update_usercard(
            card_id=card_id,
            interval=updated_data["interval"],
            state=updated_data["state"],
            due_date=updated_data["due_date"],
        )
        self.add_review(
            state=updated_data["state"], previous_state=previous_state, user_id=user_id
        )

    def handle_valid_form(self, form, active_card, card_id, user_id, context):
        """Verarbeitet die Eingabe, wenn das Formular gültig ist."""
        user_input = form.cleaned_data["card_word_name"]
        previous_state = active_card["state"]
        previous_interval = active_card["interval"]
        user_steps = self.prepare_user_steps(user_id)

        # Verarbeite richtige oder falsche Antwort
        if user_input == active_card["word__lemma"]:
            updated_data = self._handle_correct_answer(
                previous_interval, user_steps, active_card["ease"]
            )
            template = "review/answer_correct.html"
        else:
            updated_data = self._handle_incorrect_answer(previous_state, user_steps)
            template = "review/answer_incorrect.html"
            context["user_input"] = user_input
        # Aktualisiere die Karten- und Benutzerinformationen
        self._update_usercard_and_review(
            card_id=card_id,
            previous_state=previous_state,
            updated_data=updated_data,
            user_id=user_id,
        )
        context = self._build_context_for_next_page(context, active_card, updated_data)
        return render(self.request, template, context)


class ReviewView(ReviewBaseView):
    model = Deck
    template_name = "review/review.html"
    form_class = ReviewForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        deck_id = self.kwargs["pk"]
        user = self.request.user
        cache_key = f"piechart_{user.id}"
        cache.delete(cache_key)
        due_deck = self.get_due_deck(deck_id, user)
        due_card = self.get_due_card(due_deck.id, user)
        if due_card:
            context.update(
                {
                    "due_cards": due_deck.due_cards,
                    "due_card": due_card,
                    "translation": due_card.get_joined_translation(),
                }
            )
        return context

    def post(self, request, *args, **kwargs):
        context = {}
        deck_id = self.kwargs["pk"]
        form = self.form_class(request.POST)
        card_id = request.POST.get("due_card_id")
        user_id = request.user.id

        # Hole die aktiven Karten
        active_card = self.get_active_in_progress_card(card_id)
        context["deck_id"] = deck_id
        context["due_card"] = self.get_due_card(deck_id, user_id)
        context["due_card_id"] = card_id

        # Wenn die Karte noch nicht fällig ist, zeige die leere Seite
        if not self.is_card_due(active_card):
            return self.render_empty_page(context)

        if form.is_valid():
            return self.handle_valid_form(form, active_card, card_id, user_id, context)

        # Wenn das Formular ungültig ist, zeige das ungültige Formular
        context["form"] = form
        return self.render_invalid_form(context)


class TurboReviewView(ReviewBaseView, TurboReviewMixin):
    template_name = "review/review.html"
    form_class = ReviewForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        due_card = self.get_due_card_turbo(user)
        if due_card:
            context["due_card"] = due_card
            context["due_cards"] = self.get_amount_of_all_due_cards(user)
            context["translation"] = due_card.get_joined_translation()
        return context

    def post(self, request, *args, **kwargs):
        context = {}
        form = self.form_class(request.POST)
        card_id = request.POST.get("due_card_id")
        user_id = request.user.id

        active_card = self.get_active_in_progress_card(card_id)
        context["due_card"] = self.get_due_card_turbo(user=request.user)
        context["due_card_id"] = card_id

        # Wenn die Karte noch nicht fällig ist, zeige die leere Seite
        if not self.is_card_due(active_card):
            return self.render_empty_page(context)

        if form.is_valid():
            return self.handle_valid_form(form, active_card, card_id, user_id, context)

        # Wenn das Formular ungültig ist, zeige das ungültige Formular
        context["form"] = form
        return self.render_invalid_form(context)


class SkipCardView(ReviewMixin, TemplateView):
    template_name = "review/answer_skip.html"

    def post(self, request, *args, **kwargs):
        deck_id = self.kwargs["pk"]
        context = self._get_initial_context(deck_id)
        card_id = request.POST.get("due_card_id")
        active_card = self._get_active_card_or_404(card_id)
        interval = self._update_state(active_card, card_id, request.user.id)
        context.update(
            {
                "active_card": active_card,
                "interval": interval,
                "audio": active_card["word__audio"],
            }
        )
        return render(request, self.template_name, context)

    def _get_initial_context(self, deck_id):
        """Initialisiert den Kontext mit Deck-Slug"""
        return {"deck_id": deck_id}

    def _get_active_card_or_404(self, card_id):
        """Holt die aktive Lernkarte oder gibt einen Fehler aus, wenn sie nicht gefunden wird"""
        try:
            return self.get_active_in_progress_card(card_id)
        except Card.DoesNotExist:
            raise Http404("Die angeforderte Lernkarte wurde nicht gefunden.")

    def _update_state(self, active_card, card_id, user_id):
        """Aktualisiert den Lernstatus basierend auf der aktuellen Karte und gibt den neuen Lernschritt zurück"""
        return self.update_state(
            previous_state=active_card["state"], card_id=card_id, user_id=user_id
        )
