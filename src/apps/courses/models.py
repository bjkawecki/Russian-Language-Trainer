from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from apps.courses.managers import CourseManager
from apps.users.models import User


class Course(models.Model):
    class CourseLevel(models.TextChoices):
        A0 = ("A0", "Null")
        A1 = ("A1", "Anfänger")
        A2 = ("A2", "Grundkenntnisse")
        B1 = ("B1", "Fortgeschritten")
        B2 = ("B2", "Selbständig")
        C1 = ("C1", "Fachkundig")
        C2 = ("C2", "Muttersprachennah")

    name = models.TextField(
        "Niveaustufe", max_length=2, choices=CourseLevel.choices, unique=True
    )
    user = models.ManyToManyField(User, blank=True, verbose_name="Nutzer")
    json_file = models.FileField("JSON-Datei", upload_to="json/", blank=True, null=True)
    slug = models.SlugField(max_length=2, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Course, self).save(*args, **kwargs)

    objects = CourseManager()

    class Meta:
        app_label = "courses"
        verbose_name = "Kurs"
        verbose_name_plural = "Kurse"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("course_details", kwargs={"name": self.name})

    def count_decks(self):
        return self.deck_set.count()

    def count_words(self):
        return self.word_set.count()

    def get_full_name(self):
        return f"{self.get_name_display()} ({self.name})"
