from django.db import models
from django.urls import reverse

from apps.courses.models import Course
from apps.decks.managers import DeckManager
from apps.shared.utils import custom_slugify
from apps.users.models import User


class Deck(models.Model):
    name = models.CharField("Stapelname", max_length=200)
    user = models.ManyToManyField(User, blank=True, verbose_name="Nutzer")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = custom_slugify(f"{self.name}-{self.course.name}")
        super(Deck, self).save(*args, **kwargs)

    objects = DeckManager()

    class Meta:
        app_label = "decks"
        verbose_name = "Stapel"
        verbose_name_plural = "Stapel"

    def __str__(self):
        return self.name

    def update_slug(self):
        """Aktualisiert den Slug basierend auf dem Namen."""
        new_slug = custom_slugify(self.name)
        if self.slug != new_slug:  # Verhindert unnötige Speichervorgänge
            self.slug = new_slug
            self.save()

    def is_new_deck(self):
        if self.all_cards == self.initial_cards:
            return True

    def is_due_deck(self):
        if self.due_cards > 0:
            return True

    def is_not_new_deck(self):
        if (
            self.due_in_progress_cards
            or self.due_mastered_cards
            or self.initial_cards
            and self.initial_cards != self.all_cards
        ):
            return True

    def get_absolute_url(self):
        return reverse("deck_details", kwargs={"slug": self.slug})

    def get_state(self):
        if self.initial_cards == self.all_cards:
            return "initial"
        elif self.mastered_cards == self.all_cards:
            return "mastered"
        else:
            return "in_progress"

    def count_words(self):
        return self.word_set.count()

    def count_initial_cards(self):
        return self.initial_cards

    def count_in_progress_cards(self):
        return self.in_progress_cards

    def count_mastered_cards(self):
        return self.mastered_cards

    def calc_initial_cards_percent(self):
        return round(self.initial_cards / self.all_cards * 100, 1)

    def calc_in_progress_cards_percent(self):
        return round(self.in_progress_cards / self.all_cards * 100, 1)

    def calc_mastered_cards_percent(self):
        return round(self.mastered_cards / self.all_cards * 100, 1)
