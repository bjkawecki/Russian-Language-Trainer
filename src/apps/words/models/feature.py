from django.db import models

from apps.words.models.word import Feature


class AdjectiveFeature(Feature):
    is_gradable = models.BooleanField("Steigerbar", default=False)

    class Meta:
        app_label = "words"
        verbose_name = "Adjektiv Merkmale"
        verbose_name_plural = "Adjektiv Merkmale"


class AdverbFeature(Feature):
    preposition = models.CharField("Präposition", max_lenth=50)

    class Meta:
        app_label = "words"
        verbose_name = "Adverb Merkmale"
        verbose_name_plural = "Adverb Merkmale"


class NumeralFeature(Feature):
    class NumeralType(models.TextChoices):
        CARDINAL = "cardinal", "Grundzahl"
        COLLECTING = "collecting", "Sammelzahl"
        ORDINAL = "ordinal", "Ordnungszahl"

    class DeclinationType(models.TextChoices):
        SUBSTANTIVE = "substantive", "Substantiv"
        ADJECTIVE = "adjective", "Adjektiv"

    numeral_type = models.CharField("Typ", choices=NumeralType.choices)
    declination_type = models.CharField("Deklination", choices=DeclinationType.choices)

    class Meta:
        app_label = "words"
        verbose_name = "Numerale Merkmale"
        verbose_name_plural = "Numerale Merkmale"


class PrepositionFeature(Feature):
    class PrepositionType(models.TextChoices):
        LOCAL = "local", "Ort"
        DIRECTIONAL = "directional", "Richtung"
        TEMPORAL = "temporal", "Zeit"
        CAUSAL = "causal", "Ursache"
        MODAL = "modal", "Art und Weise"

    class PrepositionCase(models.TextChoices):
        GENITIVE = "genitive", "Genitiv"
        DATIVE = "dative", "Dativ"
        ACCUSATIVE = "accusative", "Akkusativ"
        INSTRUMENTAL = "instrumental", "Instrumental"
        PREPOSITIVE = "prepositive", "Präpositiv"

    preposition_type = models.CharField("Typ", choices=PrepositionType.choices)
    preposition_case = models.CharField("Kasus", choices=PrepositionCase.choices)

    class Meta:
        app_label = "words"
        verbose_name = "Präposition Merkmale"
        verbose_name_plural = "Präposition Merkmale"


class PronounFeature(Feature):
    class PronounType(models.TextChoices):
        PERSONAL = "personal", "Personal"
        POSSESSIVE = "possessive", "Possessiv"
        DEMONSTRATIVE = "demonstrative", "Demonstrativ"
        INTERROGATIVE = "interrogative", "Interrogativ"
        RELATIVE = "relative", "Relativ"
        DEFINITE = "definite", "Definit"
        INDEFINITE = "indefinite", "Indefinit"
        NEGATION = "negation", "Negations"

    class DeclinationType(models.TextChoices):
        ADJECTIVE = "adjective", "Adjektiv"
        SUBSTANTIVE = "substantive", "Substantiv"
        NO = "no", "keine"

    pronoun_type = models.CharField("Typ", choices=PronounType.choices)
    declination_type = models.CharField("Deklination", choices=DeclinationType.choices)

    class Meta:
        app_label = "words"
        verbose_name = "Pronomen Merkmale"
        verbose_name_plural = "Pronomen Merkmale"


class SubstantiveFeature(Feature):
    class Genus(models.TextChoices):
        MAS = "masculine", "Maskulinum"
        FEM = "feminine", "Femininum"
        NEU = "neutral", "Neutrum"
        NO = "no", "kein Geschlecht"

    class DeclinationClass(models.TextChoices):
        CLS1 = "1", "Klasse I"
        CLS2 = "2", "Klasse II"
        CLS3 = "3", "Klasse III"
        CLS4 = "adjective", "adjektivisch"
        CLS5 = "irregular", "unregelmäßig"
        CLS6 = "none", "keine"

    class Stress(models.TextChoices):
        ROOT = "root", "Stamm"
        SUFFIX = "suffix", "Endung"
        SHIFTING = "shifting", "Wechsel"

    genus = models.CharField("Genus", choices=Genus.choices)
    declination_class = models.CharField(
        "Deklinationsklasse", choices=DeclinationClass.choices
    )
    stress = models.CharField("Betonung", choices=Stress.choices)
    is_alive = models.BooleanField("Belebt", default=False)
    is_singular_tantum = models.BooleanField("Singularwort", default=False)
    is_plural_tantum = models.BooleanField("Pluralwort", default=False)

    class Meta:
        app_label = "words"
        verbose_name = "Substantiv Merkmale"
        verbose_name_plural = "Substantiv Merkmale"


class VerbFeature(Feature):
    class Aspect(models.TextChoices):
        PERFECTIVE = "perfective", "vollendet"
        IMPERFECTIVE = "imperfective", "unvollendet"
        DUAL = "dual", "dual"

    class ConjugationClass(models.TextChoices):
        E_CONJUGATION = "e", "E-Konjugation"
        I_CONJUGATION = "i", "I-Konjugation"
        IRREGULAR = "irregular", "unregelmäßig"

    class Direction(models.TextChoices):
        UNIDIRECTIONAL = "unidirectional", "zielgerichtet"
        MULTIDIRECTIONAL = "multidirectional", "nicht zielgerichtet"

    class ObjectCase(models.TextChoices):
        GENITIVE = "genitive", "Genitiv"
        DATIVE = "dative", "Dativ"
        ACCUSATIVE = "accusative", "Akkusativ"
        INSTRUMENTAL = "instrumental", "Instrumental"
        PREPOSITIVE = "prepositive", "Präpositiv"

    aspect = models.CharField("Aspekt", choices=Aspect.choices)
    aspect_partner = models.CharField("Aspektpartner", blank=True)
    conjugation_class = models.CharField(
        "Konjugationsklasse", choices=ConjugationClass.choices
    )
    is_motion_verb = models.BooleanField("Verb der Bewegung", default=False)
    motion_partner = models.CharField("Bewegungspartner", blank=True)
    direction = models.CharField("Richtung", blank=True, choices=Direction.choices)
    direct_object_case = models.CharField(
        "Kasus Objekt", blank=True, choices=ObjectCase.choices
    )
    indirect_object_case = models.CharField(
        "Indirektes Kasus Objekt", blank=True, choices=ObjectCase.choices
    )
    direct_object_preposition = models.CharField("Präseposition", blank=True)
    indirect_object_preposition = models.CharField("Präseposition", blank=True)
    is_reflexive = models.BooleanField("Reflexiv", default=False)
    irregular_conjugation = models.BooleanField(
        "Unregelmäßige Konjugation", default=False
    )

    class Meta:
        app_label = "words"
        verbose_name = "Verb Merkmale"
        verbose_name_plural = "Verb Merkmale"
