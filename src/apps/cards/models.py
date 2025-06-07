import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone

from apps.cards.enums import CardState
from apps.cards.managers import CardManager
from apps.users.models import User
from apps.words.models.translation import Translation
from apps.words.models.word import Word


class Card(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    word = models.ForeignKey(
        Word, verbose_name="Karte", on_delete=models.CASCADE, null=True
    )
    due_date = models.DateTimeField(auto_now_add=True)
    state = models.CharField(
        "Lernstatus", choices=CardState.choices, default=CardState.INITIAL
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Nutzer", null=True
    )
    ease = models.IntegerField(
        default=170, validators=[MaxValueValidator(250), MinValueValidator(130)]
    )
    interval = models.IntegerField(default=0, verbose_name="Lernschritt")

    objects = CardManager()

    class Meta:
        app_label = "cards"
        ordering = ["word__lemma"]
        verbose_name = "Karte"
        verbose_name_plural = "Karten"

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse("card_details", kwargs={"slug": self.word.slug})

    def get_joined_translation(self):
        translations = (
            Translation.objects.select_related("cards")
            .filter(words=self.word)
            .order_by("id")
            .values_list("name", flat=True)
            .distinct()
        )
        joined_translation = ", ".join(list(translations))
        return joined_translation

    def is_due(self):
        if self.due_date < timezone.now():
            return True
        else:
            return False
