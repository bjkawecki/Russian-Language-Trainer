from calendar import LocaleHTMLCalendar
from datetime import date, datetime

from apps.proverbs.models import Proverb
from apps.reviews.models import Review


class WidgetsMixin:
    def get_review_context(self, user):
        """Get data about reviewed cards."""
        context = {}
        try:
            review = Review.objects.get(user__id=user.id, date=date.today())
            context["reviewed_cards"] = review.reviewed_cards
        except Review.DoesNotExist:
            context["reviewed_cards"] = Review.objects.none()
        return context

    def get_daily_proverb(self, user):
        """Gibt das Tages-Sprichwort des Nutzers zurück und aktualisiert es, falls nötig."""
        today = date.today()

        if user.daily_proverb and user.daily_proverb_updated == today:
            return {"proverb": user.daily_proverb}

        new_daily_proverb = self._select_new_proverb(user)
        self._update_user_proverb(user, new_daily_proverb, today)

        return {"proverb": new_daily_proverb}

    def _select_new_proverb(self, user):
        """Wählt ein neues Sprichwort aus, das nicht dem aktuellen entspricht."""
        if not user.daily_proverb:
            return Proverb.objects.order_by("?").first()

        return (
            Proverb.objects.exclude(proverb_id=user.daily_proverb.proverb_id)
            .order_by("?")
            .first()
        )

    def _update_user_proverb(self, user, new_proverb, today):
        """Aktualisiert das Sprichwort und das Datum des Nutzers."""
        user.daily_proverb = new_proverb
        user.daily_proverb_updated = today
        user.save()


class CalendarMixin(LocaleHTMLCalendar):
    """Generates the calendar for the current month."""

    def __init__(self, *args, **kwargs):
        """Initialize with the current month and year."""
        self.year, self.month = self.get_current_month_and_year()
        super().__init__(*args, **kwargs)

    def get_current_month_and_year(self):
        """Provides the current month and year."""
        now = datetime.now()
        return now.year, now.month

    def get_user_reviews(self, user):
        return Review.objects.filter(
            date__year=self.year, date__month=self.month, user=user
        )

    def _get_css_classes_for_day(self, day, reviews):
        """Determine CSS classes for a single day."""
        is_today = date.today().day == day
        has_reviews = any(review.date.day == day for review in reviews)

        today_classes = (
            "font-bold text-blue-400 dark:text-white "
            if is_today
            else "dark:border-gray-800 border-white"
        )
        review_classes = "bg-blue-500 rounded-full text-white" if has_reviews else ""

        return f"{review_classes} {today_classes}"

    def formatday(self, day, reviews):
        """Formats a single day cell with relevant CSS classes."""
        if day == 0:  # Empty cell for padding
            return "<td class='text-center rounded-full border border-white dark:border-gray-800'></td>"
        css_classes = self._get_css_classes_for_day(day, reviews)
        return f"<td class='text-center border rounded-full {css_classes}'>{day}</td>"

    def formatweek(self, current_week, reviews):
        """Formats a week row with all days."""
        week = "".join(self.formatday(day, reviews) for day, _ in current_week)
        return f"<tr class='text-sm text-center'> {week} </tr>"

    def formatmonth(self, user, withyear=True):
        """Generates the complete HTML for the calendar."""
        reviews = self.get_user_reviews(user)
        cal = (
            '<table class="w-full table-fixed" style="border-spacing: 3px; border-collapse: separate;">\n'
            f"{self.formatmonthname(self.year, self.month, withyear=withyear)}\n"
            f"{self.formatweekheader()}\n"
        )
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f"{self.formatweek(week, reviews)}\n"
        cal += "</table>"
        return cal

    def get_calendar_context(self, user):
        html_cal = self.formatmonth(user, withyear=True)
        return {"calendar": html_cal}
