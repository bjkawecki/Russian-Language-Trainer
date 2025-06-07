from collections import namedtuple
from datetime import date as datetimedate
from datetime import datetime, timedelta

from django.db.models import Count, F, Max, Q
from django.utils import timezone

from apps.cards.enums import CardState
from apps.cards.models import Card
from apps.decks.models import Deck
from apps.reviews.models import Review
from apps.users.models import Step

NextState = namedtuple("NextState", ["due_date", "interval", "state"])


class TurboReviewMixin:
    def _get_userdecks(self, user):
        return (
            Deck.objects.count_due_cards(user)
            .filter(user=user)
            .alias(latest_usercard=Max("word__card__due_date"))
        )

    def get_duedecks(self, user):
        return (
            self._get_userdecks(user)
            .order_by("latest_usercard")
            .exclude(Q(all_cards=F("initial_cards")) | Q(due_cards=0))
        )


class ReviewMixin:
    DEFAULT_EASE = 170
    RESET_HOUR = 4
    MINUTES_PER_DAY = 1440

    def get_amount_of_all_due_cards(self, user):
        deck_ids = self._get_due_deck_ids(user)
        if not deck_ids:
            return 0
        count = Card.objects.filter(
            user=user, due_date__lte=timezone.now(), word__deck__id__in=deck_ids
        ).count()
        return count

    def _get_due_deck_ids(self, user):
        now = timezone.now()
        return list(
            Deck.objects.filter(user=user)
            .annotate(
                due_cards=Count(
                    "word",
                    filter=(
                        Q(word__card__due_date__lte=now)
                        & Q(
                            word__card__state__in=[
                                CardState.IN_PROGRESS,
                                CardState.MASTERED,
                            ]
                        )
                        & Q(word__card__user=user)  # WICHTIG: hier korrekt user binden
                    ),
                    distinct=True,
                )
            )
            .filter(due_cards__gt=0)
            .values_list("id", flat=True)
        )

    def get_due_deck(self, deck_id, user):
        return Deck.objects.count_cards(user).filter(id=deck_id).first()

    def get_due_card(self, due_deck_id, user):
        return (
            Card.objects.select_related("word__deck", "word", "user")
            .filter(word__deck__id=due_deck_id, user=user, due_date__lte=timezone.now())
            .order_by("due_date")
            .first()
        )

    def get_due_card_turbo(self, user):
        due_decks = (
            Deck.objects.count_due_cards(user)
            .filter(user=user)
            .alias(latest_usercard=Max("word__card__due_date"))
            .order_by("latest_usercard")
            .exclude(Q(all_cards=F("initial_cards")) | Q(due_cards=0))
        )

        return (
            Card.objects.select_related("word__deck", "word", "user")
            .filter(user=user, due_date__lte=timezone.now(), word__deck__in=due_decks)
            .order_by("due_date")
            .first()
        )

    def humanize_interval(self, interval):
        return self._humanize_interval_duration(interval=interval)

    def _humanize_interval_duration(self, interval):
        if interval < 60:
            return f"{interval} Minuten"
        elif interval == 60:
            return "1 Stunde"
        elif interval < 1440:
            return f"{interval // 60} Stunden"
        elif interval == 1440:
            return "1 Tag"
        else:
            return f"{int(interval // 1440)} Tage"

    def get_active_in_progress_card(self, card_id):
        return (
            Card.objects.select_related("word")
            .values(
                "id",
                "word__audio",
                "interval",
                "word__lemma",
                "word__lemma_accent",
                "state",
                "ease",
                "due_date",
            )
            .get(id=card_id)
        )

    def _get_user_steps(self, user_id):
        user_steps = list(
            Step.objects.filter(user_id=user_id).values_list("step", flat=True)
        )
        user_steps.insert(0, 0)  # Ensure the initial step is included
        user_steps.sort()
        return user_steps

    def _calculate_next_state(self, previous_state, user_steps):
        if previous_state == CardState.INITIAL:
            return NextState(timezone.now(), user_steps[0], CardState.IN_PROGRESS)
        elif previous_state == CardState.IN_PROGRESS:
            return NextState(timezone.now(), user_steps[0], CardState.IN_PROGRESS)
        elif previous_state == CardState.MASTERED:
            updated_interval = user_steps[1]
            days = updated_interval / self.MINUTES_PER_DAY
            return NextState(
                timezone.now() + timedelta(days=days),
                updated_interval,
                CardState.IN_PROGRESS,
            )
        else:
            raise ValueError(
                f"Invalid in_progress state: {previous_state}. Expected one of {CardState.INITIAL}, "
                f"{CardState.IN_PROGRESS}, {CardState.MASTERED}."
            )

    def update_state(self, previous_state, card_id, user_id):
        user_steps = self._get_user_steps(user_id)
        next_state_params = self._calculate_next_state(
            previous_state, user_steps
        )._asdict()
        Card.objects.filter(id=card_id).update(**next_state_params)
        return self._humanize_interval_duration(next_state_params["interval"])

    def prepare_user_steps(self, user_id):
        """Fügt einen Standardwert hinzu und sortiert die Schritte."""
        user_steps = list(
            Step.objects.filter(user__id=user_id).values_list("step", flat=True)
        )
        user_steps = sorted(set(user_steps + [0]))
        return user_steps

    def _handle_correct_answer(self, previous_interval, user_steps, ease):
        interval = self._calculate_interval_right(previous_interval, user_steps, ease)
        state = self._determine_state(previous_interval, interval, user_steps)
        due_date = self._calculate_due_date_right(interval)
        return {"interval": interval, "state": state, "due_date": due_date}

    def _calculate_interval_right(self, previous_interval, user_steps, ease):
        """
        Berechnet den neuen Schritt basierend auf der Eingabe.

        Args:
            previous_interval: Der vorherige Schritt in Minuten.
            user_steps: Die Liste der Benutzer-Schritte.
            ease: Der Leichtigkeitsfaktor.

        Returns:
            Der aktualisierte Schritt.
        """
        for index, user_step in enumerate(user_steps):
            if previous_interval == user_step and index + 1 < len(user_steps):
                return user_steps[index + 1]
        return int(previous_interval * ease / 100)

    def _determine_state(self, previous_interval, updated_interval, user_steps):
        """
        Bestimmt den neuen Zustand basierend auf der Eingabe.

        Args:
            previous_interval: Der vorherige Schritt in Minuten.
            updated_interval: Der neue Schritt in Minuten.
            user_steps: Die Liste der Benutzer-Schritte.

        Returns:
            Der neue Zustand.
        """
        if previous_interval in user_steps and updated_interval in user_steps:
            return CardState.IN_PROGRESS
        return CardState.MASTERED

    def _calculate_due_date_right(self, updated_interval):
        """
        Berechnet das neue Fälligkeitsdatum basierend auf Zustand und Schritt.

        Args:
            updated_state: Der neue Lernstatus.
            updated_interval: Der neue Schritt in Minuten.

        Returns:
            Ein Tuple mit Fälligkeitsdatum, Zustand und Schritt.
        """
        days = updated_interval / self.MINUTES_PER_DAY
        updated_due_date = timezone.now() + timedelta(days=days)

        if updated_interval > self.MINUTES_PER_DAY:
            updated_due_date = updated_due_date.replace(
                microsecond=0, second=0, minute=0, hour=self.RESET_HOUR
            )

        return updated_due_date

    def update_usercard(self, card_id, due_date, state, interval):
        Card.objects.filter(id=card_id).update(
            due_date=due_date, state=state, interval=interval
        )

    def _handle_incorrect_answer(self, previous_state, user_steps):
        state = CardState.IN_PROGRESS
        interval = self._calculate_interval_wrong(previous_state, user_steps)
        due_date = self._calculate_due_date_wrong(previous_state, user_steps)
        return {"interval": interval, "state": state, "due_date": due_date}

    def _calculate_interval_wrong(self, previous_state, user_steps):
        """
        Berechnet das neue Intervall basierend auf dem vorherigen Zustand der Karte.
        """
        if (
            previous_state == CardState.INITIAL
            or previous_state == CardState.IN_PROGRESS
        ):
            updated_interval = user_steps[0]
        elif previous_state == CardState.MASTERED:
            updated_interval = user_steps[1]
        else:
            raise ValueError(
                f"Error in _handle_incorrect_answer(): input '{previous_state}' \
                    for variable 'due_card.state' does not match value of \
                    'Card.self'."
            )

        return updated_interval

    def _calculate_due_date_wrong(self, previous_state, user_steps):
        """
        Berechnet das neue Fälligkeitsdatum basierend auf dem vorherigen Zustand der Karte.
        """
        if (
            previous_state == CardState.INITIAL
            or previous_state == CardState.IN_PROGRESS
        ):
            return timezone.now()
        elif previous_state == CardState.MASTERED:
            updated_interval = user_steps[1]
            days = self.MINUTES_PER_DAY * updated_interval
            return timezone.now() + timedelta(days=days)
        else:
            raise ValueError(
                f"Error in _handle_incorrect_answer(): input '{previous_state}' \
                    for variable 'due_card.state' does not match value of \
                    'Card.CardState'."
            )


class ReviewUpdateError(Exception):
    """Custom exception for review update errors."""

    pass


class NewReviewMixin:
    def add_review(self, state, previous_state, user_id):
        today = datetimedate.today()
        review, created = Review.objects.get_or_create(user_id=user_id, date=today)
        review.reviewed_cards += 1
        if previous_state == CardState.INITIAL:
            review.initial_cards += 1
        elif previous_state == CardState.IN_PROGRESS:
            review.in_progress_cards += 1
        elif previous_state == CardState.MASTERED:
            review.mastered_cards += 1
        else:
            # Raising custom exception for better error handling
            raise ReviewUpdateError(
                f"Invalid new in_progress state '{state}' for user '{user_id}'."
            )
        review.save()
        return

    def get_usercards_count(self, user):
        return Card.objects.count_by_state(user)

    def get_past_month_reviews(self, user):
        return Review.objects.filter(user=user).order_by("date")[:30]

    def get_dates(self, user):
        dates = []
        delta = timedelta(days=1)
        week = timedelta(days=7)
        end_date = datetime.date(datetime.now())
        start_date = end_date - week
        while start_date <= end_date:
            dates.append(start_date.strftime("%d.%m.%Y"))
            start_date += delta
        return dates

    def get_due_cards_dates(self, due_cards, user):
        due_card_dates = []
        delta = timedelta(days=1)
        if due_cards:
            last_due_usercard = due_cards.last()
            tomorrow = timezone.now() + delta
            start_due_date = tomorrow
            end_due_date = last_due_usercard.due_date
            while start_due_date <= end_due_date:
                due_card_dates.append(start_due_date.strftime("%d.%m.%Y"))
                start_due_date += delta
        return due_card_dates

    def get_due_cards_count(self, due_card_dates, due_cards):
        due_cards_count = []
        for date in due_card_dates:
            a = 0
            for card in due_cards:
                if card.due_date.strftime("%d.%m.%Y") == date:
                    a += 1
            due_cards_count.append(a)
        return due_cards_count

    def get_usercards_per_date(self, dates, reviews):
        reviewed_cards = []
        initial_cards = []
        in_progress_cards = []
        mastered_cards = []

        for date in dates:
            review_date = 0
            new_date = 0
            in_progress_date = 0
            mastered_date = 0
            for review in reviews:
                if date == review.date.strftime("%d.%m.%Y"):
                    review_date = review.reviewed_cards
                    new_date = review.initial_cards
                    in_progress_date = review.in_progress_cards
                    mastered_date = review.mastered_cards

            reviewed_cards.append(review_date or 0)
            initial_cards.append(new_date or 0)
            in_progress_cards.append(in_progress_date or 0)
            mastered_cards.append(mastered_date or 0)

        return reviewed_cards, initial_cards, in_progress_cards, mastered_cards

    def get_heatmap_dates(self):
        heatmap_dates_iso = []
        hm_start_date = datetime(2024, 1, 1)
        hm_end_date = datetime.now()
        delta = timedelta(days=1)
        while hm_start_date <= hm_end_date:
            heatmap_dates_iso.append(hm_start_date.isocalendar())
            hm_start_date += delta
        return heatmap_dates_iso

    def get_heatmap_list(self, heatmap_dates_iso, reviews):
        def create_all_weekdays_date_list(date_generator, reviews):
            date_list = []
            for date in date_generator:
                review_int = 0
                for review in reviews:
                    if review.date.isocalendar() == date.isocalendar():
                        review_int = review.reviewed_cards
                date_list.append({"x": date.strftime("%d.%m.%Y"), "y": review_int})
            return date_list

        def get_all_weekdays_date(index, year):
            d = datetime(year, 1, 1)
            d += timedelta(days=index - d.weekday())
            while d.year == year:
                yield d
                d += timedelta(days=7)

        heatmap_obj = {}
        for date in heatmap_dates_iso:
            heatmap_obj[date.weekday] = []
        for date in heatmap_dates_iso:
            review_int = 0
            for review in reviews:
                if review.date.isocalendar() == date:
                    review_int = review.reviewed_cards
            heatmap_obj[date.weekday].append(review_int or 0)
            weekdays = [
                "Montag",
                "Dienstag",
                "Mittwoch",
                "Donnerstag",
                "Freitag",
                "Samstag",
                "Sonntag",
            ]
        heatmap_obj = dict(zip(weekdays, list(heatmap_obj.values())))

        heatmap_list = [
            {
                "name": weekday,
                "data": create_all_weekdays_date_list(
                    get_all_weekdays_date(index, 2024), reviews
                ),
            }
            for index, weekday in enumerate(weekdays)
        ]
        heatmap_list
        return heatmap_list
