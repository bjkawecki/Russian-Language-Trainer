from datetime import date, timedelta

import numpy as np
from django.db.models import Sum

from apps.reviews.models import Review


class CalendarHeatmapMixin:
    def get_heatmap_data(self, user, year=None):
        # Falls kein Jahr angegeben ist, verwende das aktuelle Jahr
        if not year:
            year = date.today().year

        # Hole die Reviews-Daten für das Jahr
        reviews = (
            Review.objects.filter(date__year=year, user=user)
            .values("date")
            .annotate(total_reviewed_cards=Sum("reviewed_cards"))
            .order_by("date")
        )

        review_dict = {rev["date"]: rev["total_reviewed_cards"] for rev in reviews}

        # Berechne den Wochentag für den 1. Januar
        first_day_of_year = date(year, 1, 1)
        first_day_weekday = first_day_of_year.weekday()  # Wochentag des 1. Januars

        days_in_year = 365 + (1 if year % 4 == 0 else 0)  # 366 Tage im Schaltjahr

        values = []
        dates = []
        hovertext = np.full((7, 53), "", dtype=object)  # Platz für Hovertext

        # Generiere die Werte, Tage und den Hovertext
        for n in range(days_in_year):
            day = first_day_of_year + timedelta(days=n)

            dates.append(day)
            review_count = review_dict.get(day, 0)  # Wenn keine Review, dann 0
            values.append(review_count)

            hovertext_day = (
                f"Datum: {day.strftime('%d.%m.%Y')} | Wiederholungen: {review_count}"
            )

            day_of_week = (n + first_day_weekday) % 7
            week_num = (n + first_day_weekday) // 7
            hovertext[day_of_week, week_num] = hovertext_day

        weeks = np.zeros((7, 53))  # Wochentage als Zeilen, Wochen als Spalten

        for i, value in enumerate(values):
            week_num = (i + first_day_weekday) // 7
            day_of_week = (i + first_day_weekday) % 7
            weeks[day_of_week, week_num] = value

        return weeks, hovertext, first_day_of_year

    # def create_heatmap_figure(self, weeks, hovertext, colors, year, first_day_of_year, color_mode):
    #     if color_mode == "dark":
    #         font_color = "white"
    #         plot_bgcolor = "rgb(50,60,72)"
    #         paper_bgcolor = "rgb(0,0,0,0)"
    #         custom_colorscale = [
    #             (0.0, "rgb(34,40,49)"),
    #             (0.01, "rgb(123,200,254)"),
    #             (0.50, "rgb(11,147,236)"),
    #             (0.75, "rgb(5, 117, 196)"),
    #             (1.0, "rgb(0,87,156)"),
    #         ]

    #     else:
    #         font_color = "black"
    #         plot_bgcolor = "white"
    #         paper_bgcolor = "rgb(0,0,0,0)"
    #         custom_colorscale = [
    #             (0.0, "rgb(210, 211, 212)"),
    #             (0.01, "rgb(123,200,254)"),
    #             (0.50, "rgb(11,147,236)"),
    #             (0.75, "rgb(5, 117, 196)"),
    #             (1.0, "rgb(0,87,156)"),
    #         ]

    #     fig = go.Figure(
    #         go.Heatmap(
    #             z=weeks,
    #             colorscale=custom_colorscale,
    #             showscale=False,
    #             xgap=2,
    #             ygap=2,
    #             hovertext=hovertext,
    #             hoverinfo="text",
    #             zmin=0,
    #             zmax=100,
    #             customdata=colors,
    #         )
    #     )

    #     month_labels = ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]

    #     month_positions = [((date(year, month, 1) - first_day_of_year).days // 7) + 2 for month in range(1, 13)]

    #     fig.update_layout(
    #         title=None,
    #         xaxis=dict(
    #             tickmode="array",
    #             tickvals=month_positions,
    #             ticktext=month_labels,
    #             title=None,
    #             showgrid=False,
    #             zeroline=False,
    #             title_font=dict(family="Arial", size=14, color=font_color),
    #             tickfont=dict(family="Arial", size=12, color=font_color),
    #         ),
    #         yaxis=dict(
    #             tickmode="array",
    #             tickvals=list(range(7)),
    #             ticktext=["Mo  ", "Di  ", "Mi  ", "Do  ", "Fr  ", "Sa  ", "So  "],
    #             title=None,
    #             showgrid=False,
    #             zeroline=False,
    #             title_font=dict(family="Arial", size=14, color=font_color),
    #             tickfont=dict(family="Arial", size=12, color=font_color),
    #         ),
    #         width=768,
    #         height=160,
    #         plot_bgcolor=plot_bgcolor,
    #         margin=dict(l=0, r=0, t=30, b=0),
    #         paper_bgcolor=paper_bgcolor,
    #     )

    #     return fig
