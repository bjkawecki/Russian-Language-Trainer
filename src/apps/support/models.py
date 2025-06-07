from django.db import models

from apps.users.models import User


class UserMessage(models.Model):
    class Topic(models.IntegerChoices):
        REPORT_A_BUG = (1, "Ich möchte einen Fehler melden.")
        SOMETHING_ELSE = (2, "Etwas anderes")
        PROPOSAL = (3, "Ich möchte einen Verbesserungsvorschlag machen.")

    user = models.ForeignKey(User, models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField("Titel", max_length=100)
    content = models.TextField("Nachricht", max_length=500)
    topic = models.IntegerField(
        "Thema", choices=Topic.choices, default=Topic.SOMETHING_ELSE
    )

    class Meta:
        app_label = "support"
        verbose_name = "Nutzer-Nachricht"
        verbose_name_plural = "Nutzer-Nachrichten"

    def __str__(self):
        return f"{self.user} – {self.created_at}"
