from django.db import models


class CardState(models.TextChoices):
    INITIAL = ("initial", "neu")
    IN_PROGRESS = ("in_progress", "aktiv")
    MASTERED = ("mastered", "gemeistert")
    REVIEW = ("review", "üben")
