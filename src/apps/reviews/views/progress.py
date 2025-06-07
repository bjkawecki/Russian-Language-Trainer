import locale
from datetime import date, timedelta

import numpy as np
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum
from django.http import JsonResponse
from django.utils import timezone
from django.utils.timezone import now
from django.views.generic import TemplateView, View

from apps.cards.models import Card
from apps.reviews.mixins.piechart import PiechartMixin
from apps.reviews.models import Review


class ProgressView(LoginRequiredMixin, TemplateView, PiechartMixin):
    template_name = "progress/progress.html"

    def get_context_data(self, **kwargs):
        user = self.request.user
        one_year_ago = now() - timedelta(days=365)

        # Summiere alle reviewed_cards der letzten 12 Monate für den Benutzer
        total_reviewed_cards = (
            Review.objects.filter(user=user, date__gte=one_year_ago).aggregate(
                Sum("reviewed_cards")
            )["reviewed_cards__sum"]
            or 0
        )
        days = 30
        today = timezone.now().date()
        dates = [
            today - timedelta(days=i) for i in range(days)
        ]  # Datum als String für JSON
        month = [str(date.strftime("%d.%m.%Y")) for date in [dates[0], dates[-1]]]
        context = super().get_context_data(**kwargs)
        context["current_year"] = date.today().year
        context["month"] = month
        context["total_reviewed_cards"] = total_reviewed_cards
        context["courses"] = self.get_course_choices(user)
        context["todays_review"] = Review.objects.filter(
            user=user, date=date.today()
        ).first()
        return context


LABEL_MAPPING = {
    "initial": "Neu",
    "in_progress": "Aktiv",
    "mastered": "Gemeistert",
}


# Alle möglichen Status-Werte
ALL_STATES = ["initial", "in_progress", "mastered"]


class PiechartComponentView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        course = request.GET.get(
            "course", None
        )  # Kurs-ID aus der URL-Abfrage erhalten (falls vorhanden)
        # Karten nach Status gruppieren und zählen
        cards = Card.objects.filter(user=user)
        if course:
            cards = cards.filter(
                word__course=course
            )  # Falls Kurs ausgewählt, danach filtern

        cards_by_state = cards.values("state").annotate(count=Count("id"))
        counts = {entry["state"]: entry["count"] for entry in cards_by_state}

        # Labels und Werte erstellen
        labels = [LABEL_MAPPING.get(state, state) for state in ALL_STATES]
        values = [counts.get(state, 0) for state in ALL_STATES]

        # JSON-Daten vorbereiten
        data = {"labels": labels, "values": values}
        return JsonResponse(data)


class HeatmapComponentView(LoginRequiredMixin, View):
    def get_heatmap_data(self, user):
        today = timezone.now().date()

        # 📌 Startdatum = Der letzte Sonntag vor einem Jahr
        start_date = today - timedelta(days=365)
        start_date -= timedelta(
            days=start_date.weekday() + 1
        )  # Gehe zurück bis zum Sonntag

        next_sunday = today + timedelta(
            days=(6 - today.weekday())
        )  # Nächster Sonntag (einschließlich heute, falls Sonntag)
        remaining_days_until_sunday = (next_sunday - today).days

        # 📌 Anzahl der Tage (365 oder 366)
        num_days = (today - start_date).days + remaining_days_until_sunday

        # 📌 Review-Daten abrufen
        reviews = (
            Review.objects.filter(date__range=[start_date, today], user=user)
            .values("date")
            .annotate(total_reviewed_cards=Sum("reviewed_cards"))
            .order_by("date")
        )
        review_dict = {rev["date"]: rev["total_reviewed_cards"] for rev in reviews}

        # 📌 Heatmap-Matrix (7 Zeilen für Wochentage, 53 Spalten für Wochen)
        num_weeks = (num_days // 7) + (
            1 if num_days % 7 != 0 else 0
        )  # Berechne benötigte Spalten
        weeks = np.zeros((7, num_weeks))  # Initialisiere mit Nullen
        hovertext = np.full((7, num_weeks), "", dtype=object)

        # 🔄 Werte für die Heatmap füllen
        for n in range(num_days):
            day = start_date + timedelta(days=n)
            review_count = review_dict.get(day, 0)
            # Wenn das Datum in der Zukunft liegt, setze den Wert auf -1
            if day > today:
                review_count = -1

            week_num = n // 7  # Spaltenindex (Woche)
            day_of_week = n % 7  # Zeilenindex (Wochentag)

            weeks[day_of_week, week_num] = review_count
            if day <= today:
                hovertext[day_of_week, week_num] = (
                    f"Datum: {day.strftime('%d.%m.%Y')} | Wiederholungen: {review_count}"
                )

        # 📊 Rückgabe als JSON
        return weeks.tolist(), hovertext.tolist(), start_date.isoformat()

    def get(self, request, *args, **kwargs):
        user = request.user

        # Heatmap-Daten berechnen
        weeks, hovertext, start_date = self.get_heatmap_data(user)

        data = {
            "weeks": weeks,
            "hovertext": hovertext,
            "start_date": start_date,  # Korrekte Übergabe des 1. Januar
        }
        return JsonResponse(data)


class BarchartComponentJsonView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        today = timezone.now().date()
        days = 30

        offset = int(
            request.GET.get("offset", 0)
        )  # z.B. -1 für zurück, +1 für vorwärts
        start_date = today - timedelta(days=(offset + 1) * days)
        end_date = today - timedelta(days=offset * days)  # End des Zeitraums

        reviews = Review.objects.filter(
            date__gte=start_date, date__lte=end_date
        ).order_by("date")

        # 📊 Daten vorbereiten
        dates = [start_date + timedelta(days=i) for i in range(days + 1)]
        initial_cards = []
        in_progress_cards = []
        mastered_cards = []

        for d in dates:
            review = reviews.filter(date=d).first()
            initial_cards.append(review.initial_cards if review else 0)
            in_progress_cards.append(review.in_progress_cards if review else 0)
            mastered_cards.append(review.mastered_cards if review else 0)

        month = [str(date.strftime("%d.%m.%Y")) for date in [dates[0], dates[-1]]]

        locale.setlocale(
            locale.LC_TIME, "de_DE.UTF-8"
        )  # Deutsch für die Datumsformatierung
        # 📊 JSON-Antwort senden
        context = {
            "dates": dates[::-1],
            "initial_cards": initial_cards[::-1],
            "in_progress_cards": in_progress_cards[::-1],
            "mastered_cards": mastered_cards[::-1],
            "month": month,
            "today": str(timezone.now().date()),
            "end_date": str(end_date),
        }
        return JsonResponse(context)
