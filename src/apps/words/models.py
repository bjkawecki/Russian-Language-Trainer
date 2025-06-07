from django.db import models
from django.db.models import F, Func
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils.html import mark_safe
from django.utils.text import slugify
from polymorphic.models import PolymorphicModel

from apps.courses.models import Course
from apps.decks.models import Deck
from apps.shared.validators import cyrillic_validator
from apps.users.models import User


class Word(models.Model):
    class WordClass(models.TextChoices):
        ADJECTIVE = "adjective", "Adjektiv"
        ADVERB = "adverb", "Adverb"
        COMPOUND = "compound", "Kompositum"
        CONJUNCTION = "conjunction", "Konjunktion"
        INTERJECTION = "interjection", "Interjektion"
        NUMERAL = "numeral", "Numerale"
        PARTICLE = "particle", "Partikel"
        PHRASE = "phrase", "Phrase"
        PREPOSITION = "preposition", "Präposition"
        PRONOUN = "pronoun", "Pronomen"
        SUBSTANTIVE = "substantive", "Substantiv"
        VERB = "verb", "Verb"

    class Usage(models.TextChoices):
        SOPHISTICATED = "sophisticated", "gehoben"
        COLLOQUIAL = "colloquial", "umgangssprachlich"
        FORMAL = "formal", "förmlich"
        MAT = "mat", "Mat"
        ARCHAIC = "archaic", "veraltet"
        POETIC = "poetic", "poetisch"
        TERM = "term", "Fachwort"
        ABRREVIATION = "abbreviation", "Abkürzung"

    class Origin(models.TextChoices):
        GERMAN = "German", "Deutsch"
        ENGLISH = "English", "Englisch"
        FRENCH = "French", "Französisch"
        TURKISH = "Turkish", "Türkisch"
        PERSIAN = "Persian", "Persisch"
        DUTCH = "Dutch", "Niederländisch"
        ARABIAN = "Arabian", "Arabisch"
        ITALIAN = "Italian", "Italienisch"
        LATIN = "Latin", "Latein"
        GREEK = "Greek", "Altgriechisch"
        CHURCH_SLAVONIC = "Church Slavonic", "Kirchenlslawisch"

    lemma = models.CharField(
        "Lemma", max_length=255, validators=[cyrillic_validator], unique=False
    )
    lemma_accent = models.CharField(
        "Lemma mit Betonung",
        max_length=255,
        validators=[cyrillic_validator],
        unique=False,
    )
    transcription = models.CharField("Transkription", max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    unique_name = models.CharField("Unique Name", max_length=255, unique=True)
    wordclass = models.CharField("Wortart", choices=WordClass.choices)
    created_on = models.DateTimeField("Erstellt", auto_now_add=True)
    updated_on = models.DateTimeField("Bearbeitet", auto_now=True)
    audio = models.FileField("Audiodatei", upload_to="audio/", blank=True)
    comment = models.TextField("Kommentar", blank=True)
    usage = models.CharField("Gebrauch", blank=True, choices=Usage.choices)
    origin = models.CharField("Herkunft", choices=Origin.choices, blank=True)

    course = models.ForeignKey(
        Course, verbose_name="Kurs", on_delete=models.CASCADE, null=True, blank=True
    )
    deck = models.ForeignKey(
        Deck, verbose_name="Stapel", on_delete=models.CASCADE, null=True, blank=True
    )
    user = models.ManyToManyField(User, verbose_name="Nutzer", blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.transcription)
            slug = base_slug
            counter = 2

            # Eindeutigen Slug generieren
            while Word.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        # Wenn unique_name nicht gesetzt ist, generiere es
        if not self.unique_name:
            base_unique_name = self.lemma
            unique_name = base_unique_name
            counter = 2

            # Prüfe, ob der unique_name bereits existiert
            while Word.objects.filter(unique_name=unique_name).exists():
                # Erhöhe den Zähler und generiere den nächsten unique_name
                unique_name = f"{base_unique_name}-{counter}"
                counter += 1

            # Setze den gefundenen unique_name
            self.unique_name = unique_name

        # Speichere das Objekt
        super(Word, self).save(*args, **kwargs)

    @property
    def sound_display(self):
        if not self.audio:
            return ""
        return mark_safe(
            f"<audio controls name='media'><source src='{self.audio.url}' \
                type='audio/ogg'></audio>"
        )

    class Meta:
        app_label = "words"
        ordering = ["unique_name"]
        ordering = [Func(F("unique_name"), function="LOWER")]
        verbose_name = "Wort"
        verbose_name_plural = "Wörter"

    def __str__(self):
        return self.unique_name


class Inflection(PolymorphicModel):
    word = models.OneToOneField(
        Word, on_delete=models.CASCADE, verbose_name="Wort", blank=True, null=True
    )

    class Meta:
        app_label = "words"
        # base_manager_name = "non_polymorphic"
        verbose_name = "Flexion"
        verbose_name_plural = "Flexionen"

    def __str__(self):
        return self.word.lemma


@receiver(pre_delete, sender=Word)
def auto_delete_inflection_with_word(sender, instance, **kwargs):
    try:
        inflection = instance.inflection
    except AttributeError:
        return

    try:
        inflection._state.fields_cache = {}
    except AttributeError:
        pass

    try:
        inflection.word  # one extra query
    except AttributeError:
        # This is cascaded delete
        return

    inflection.delete()


class Feature(PolymorphicModel):
    word = models.OneToOneField(
        Word, on_delete=models.CASCADE, verbose_name="Wort", blank=True, null=True
    )

    # non_polymorphic = models.Manager()

    class Meta:
        app_label = "words"
        # base_manager_name = "non_polymorphic"
        verbose_name = "Merkmale"
        verbose_name_plural = "Merkmale"

    def __str__(self):
        return self.word.lemma


@receiver(pre_delete, sender=Word)
def auto_delete_feature_with_word(sender, instance, **kwargs):
    try:
        feature = instance.feature
    except AttributeError:
        return

    try:
        feature._state.fields_cache = {}
    except AttributeError:
        pass

    try:
        feature.word  # one extra query
    except AttributeError:
        # This is cascaded delete
        return

    feature.delete()
