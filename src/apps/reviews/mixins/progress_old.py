from datetime import date as datetimedate
from datetime import datetime, timedelta

from django.utils import timezone

from apps.cards.enums import CardState
from apps.cards.models import Card
from apps.reviews.models import Review


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
