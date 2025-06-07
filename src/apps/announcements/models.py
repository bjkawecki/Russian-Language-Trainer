import datetime
import uuid

from django.db import models
from django.utils.timezone import localdate, localtime

from apps.users.models import User


class Announcement(models.Model):
    class Category(models.IntegerChoices):
        EVENT = (1, "Neuigkeit")
        REMINDER = (2, "Erinnerung")
        SYSTEM_MESSAGE = (3, "Warnung")

    title = models.CharField("Titel", max_length=100, unique=True)
    message = models.TextField("Nachricht", max_length=2000)
    is_active = models.BooleanField("Aktiv", default=False)
    category = models.IntegerField(
        "Katagorie", choices=Category.choices, blank=True, null=True
    )
    starting_at = models.DateTimeField(blank=True, null=True, verbose_name="Startzeit")

    class Meta:
        app_label = "announcements"
        verbose_name = "Benachrichtigung"
        verbose_name_plural = "Mitteilungen"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        is_new = not self.pk
        super().save(*args, **kwargs)
        if is_new:
            users = User.objects.filter(is_active=True)
            for user in users:
                UserAnnouncement.objects.create(user=user, announcement=self)

    def get_date_label(self):
        now = localtime()  # Aktuelle Zeit in der lokalen Zeitzone
        event_time = localtime(
            self.starting_at
        )  # Zeitstempel in lokale Zeit konvertieren
        today = localdate()
        if now - datetime.timedelta(minutes=5) <= event_time <= now:
            return "gerade eben"
        elif event_time.date() == today:
            return "heute"
        elif event_time.date() == today - datetime.timedelta(days=1):
            return "gestern"
        else:
            return event_time.strftime("%d.%m.%Y")  # Formatierte Anzeige


class UserAnnouncement(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    announcement = models.ForeignKey(
        Announcement, on_delete=models.CASCADE, blank=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    marked_as_read = models.BooleanField("gelesen", default=False)

    class Meta:
        app_label = "announcements"
        verbose_name = "Nutzer-Benachrichtigung"
        verbose_name_plural = "Nutzer-Mitteilungen"
