from django.db import models

from apps.shared.validators import latin_validator
from apps.words.models.word import Word


class Translation(models.Model):
    words = models.ManyToManyField(Word, blank=True, verbose_name="Wort")
    name = models.CharField("Übersetzung", max_length=255, validators=[latin_validator])

    class Meta:
        app_label = "words"
        verbose_name = "Übersetzung"
        verbose_name_plural = "Übersetzungen"

    def __str__(self):
        return self.name
