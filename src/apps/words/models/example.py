from django.db import models

from apps.shared.validators import cyrillic_validator, latin_validator
from apps.words.models.word import Word


class Example(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    russian = models.TextField(
        "Beispielsatz Russisch", validators=[cyrillic_validator], blank=False, null=True
    )
    german = models.TextField(
        "Beispielsatz Deutsch", validators=[latin_validator], blank=False, null=True
    )

    class Meta:
        app_label = "words"
        verbose_name = "Beispiel"
        verbose_name_plural = "Beispiele"

    def __str__(self):
        return f'Example of "{self.word}"'
