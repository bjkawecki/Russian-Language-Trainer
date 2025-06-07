from django.db import models

from apps.users.models import User


class Review(models.Model):
    user = models.ForeignKey(User, models.CASCADE, blank=True, null=True)
    date = models.DateField()
    reviewed_cards = models.IntegerField(default=0, verbose_name="Karten pro Tag")
    initial_cards = models.IntegerField(default=0, verbose_name="Neue Karten pro Tag")
    in_progress_cards = models.IntegerField(
        default=0, verbose_name="Wiederholte Karten pro Tag"
    )
    mastered_cards = models.IntegerField(
        default=0, verbose_name="Graduierte Karten pro Tag"
    )
    passed_cards = models.IntegerField(
        default=0, verbose_name="Richtig beantwortete Karten pro Tag"
    )
    failed_cards = models.IntegerField(
        default=0, verbose_name="Falsch beantwortete Karten pro Tag"
    )

    class Meta:
        app_label = "reviews"
        verbose_name = "Wiederholung"
        verbose_name_plural = "Wiederholungen"
        indexes = [models.Index(fields=["user", "date"])]

    def __str__(self):
        return f"{self.user} – {self.date}"
