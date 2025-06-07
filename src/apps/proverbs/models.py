from django.db import models

from apps.shared.validators import cyrillic_validator, latin_validator


class Proverb(models.Model):
    proverb_id = models.IntegerField(
        "ID", primary_key=True, blank=False, editable=False, unique=True, null=False
    )
    proverb = models.TextField(
        "Sprichwort", validators=[cyrillic_validator], blank=True, null=True
    )
    translation = models.TextField(
        "Übersetzung", validators=[latin_validator], blank=True, null=True
    )
    explanation = models.TextField(
        "Erklärung", validators=[latin_validator], blank=True, null=True
    )
    equivalent = models.TextField(
        "Entsprechung", validators=[latin_validator], blank=True, null=True
    )

    class Meta:
        app_label = "proverbs"
        verbose_name = "Sprichwort"
        verbose_name_plural = "Sprichwörter"

    def __str__(self):
        return str(self.proverb)
