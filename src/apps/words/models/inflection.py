from django.db import models

from apps.words.models.word import Inflection


class NumeralInflection(Inflection):
    class NumeralType(models.TextChoices):
        CARDINAL = "cardinal", "Grundzahl"
        COLLECTING = "collecting", "Sammelzahl"
        ORDINAL = "ordinal", "Ordnungszahl"

    class DeclinationType(models.TextChoices):
        SUBSTANTIVE = "substantive", "Substantiv"
        ADJECTIVE = "adjective", "Adjektiv"

    masculine_nominative = models.CharField("Nominativ", blank=True)
    masculine_genitive = models.CharField("Genitiv", blank=True)
    masculine_dative = models.CharField("Dativ", blank=True)
    masculine_accusative = models.CharField("Akkusativ", blank=True)
    masculine_instrumental = models.CharField("Instrumental", blank=True)
    masculine_prepositive = models.CharField("Präpositiv", blank=True)

    feminine_nominative = models.CharField("Nominativ", blank=True)
    feminine_genitive = models.CharField("Genitiv", blank=True)
    feminine_dative = models.CharField("Dativ", blank=True)
    feminine_accusative = models.CharField("Akkusativ", blank=True)
    feminine_instrumental = models.CharField("Instrumental", blank=True)
    feminine_prepositive = models.CharField("Präpositiv", blank=True)

    neutral_nominative = models.CharField("Nominativ", blank=True)
    neutral_genitive = models.CharField("Genitiv", blank=True)
    neutral_dative = models.CharField("Dativ", blank=True)
    neutral_accusative = models.CharField("Akkusativ", blank=True)
    neutral_instrumental = models.CharField("Instrumental", blank=True)
    neutral_prepositive = models.CharField("Präpositiv", blank=True)

    singular_nominative = models.CharField("Nominativ", blank=True)
    singular_genitive = models.CharField("Genitiv", blank=True)
    singular_dative = models.CharField("Dativ", blank=True)
    singular_accusative = models.CharField("Akkusativ", blank=True)
    singular_instrumental = models.CharField("Instrumental", blank=True)
    singular_prepositive = models.CharField("Präpositiv", blank=True)

    plural_nominative = models.CharField("Nominativ", blank=True)
    plural_genitive = models.CharField("Genitiv", blank=True)
    plural_dative = models.CharField("Dativ", blank=True)
    plural_accusative = models.CharField("Akkusativ", blank=True)
    plural_instrumental = models.CharField("Instrumental", blank=True)
    plural_prepositive = models.CharField("Präpositiv", blank=True)

    class Meta:
        app_label = "words"
        verbose_name = "Numerale Formen"
        verbose_name_plural = "Numerale Formen"

    def get_fields(self):
        return [
            (field.verbose_name, getattr(self, field.name))
            for field in NumeralInflection._meta.fields
        ]


class AdjectiveInflection(Inflection):
    masculine_nominative = models.CharField("Nominativ", blank=True)
    masculine_genitive = models.CharField("Genitiv", blank=True)
    masculine_dative = models.CharField("Dativ", blank=True)
    masculine_accusative = models.CharField("Akkusativ", blank=True)
    masculine_instrumental = models.CharField("Instrumental", blank=True)
    masculine_prepositive = models.CharField("Präpositiv", blank=True)

    feminine_nominative = models.CharField("Nominativ", blank=True)
    feminine_genitive = models.CharField("Genitiv", blank=True)
    feminine_dative = models.CharField("Dativ", blank=True)
    feminine_accusative = models.CharField("Akkusativ", blank=True)
    feminine_instrumental = models.CharField("Instrumental", blank=True)
    feminine_prepositive = models.CharField("Präpositiv", blank=True)

    neutral_nominative = models.CharField("Nominativ", blank=True)
    neutral_genitive = models.CharField("Genitiv", blank=True)
    neutral_dative = models.CharField("Dativ", blank=True)
    neutral_accusative = models.CharField("Akkusativ", blank=True)
    neutral_instrumental = models.CharField("Instrumental", blank=True)
    neutral_prepositive = models.CharField("Präpositiv", blank=True)

    plural_nominative = models.CharField("Nominativ", blank=True)
    plural_genitive = models.CharField("Genitiv", blank=True)
    plural_dative = models.CharField("Dativ", blank=True)
    plural_accusative = models.CharField("Akkusativ", blank=True)
    plural_instrumental = models.CharField("Instrumental", blank=True)
    plural_prepositive = models.CharField("Präpositiv", blank=True)

    shortform_masculine = models.CharField("Maskulinum", blank=True)
    shortform_feminine = models.CharField("Femininum", blank=True)
    shortform_neutral = models.CharField("Neutrum", blank=True)
    shortform_plural = models.CharField("Plural", blank=True)
    comparative = models.CharField("Komparativ", blank=True)
    superlative = models.CharField("Superlativ", blank=True)

    class Meta:
        app_label = "words"
        verbose_name = "Adjektiv Formen"
        verbose_name_plural = "Adjektiv Formen"

    def get_fields(self):
        return [
            (field.verbose_name, getattr(self, field.name))
            for field in AdjectiveInflection._meta.fields
        ]


class PronounInflection(Inflection):
    masculine_nominative = models.CharField("Nominativ", blank=True)
    masculine_genitive = models.CharField("Genitiv", blank=True)
    masculine_dative = models.CharField("Dativ", blank=True)
    masculine_accusative = models.CharField("Akkusativ", blank=True)
    masculine_instrumental = models.CharField("Instrumental", blank=True)
    masculine_prepositive = models.CharField("Präpositiv", blank=True)

    feminine_nominative = models.CharField("Nominativ", blank=True)
    feminine_genitive = models.CharField("Genitiv", blank=True)
    feminine_dative = models.CharField("Dativ", blank=True)
    feminine_accusative = models.CharField("Akkusativ", blank=True)
    feminine_instrumental = models.CharField("Instrumental", blank=True)
    feminine_prepositive = models.CharField("Präpositiv", blank=True)

    neutral_nominative = models.CharField("Nominativ", blank=True)
    neutral_genitive = models.CharField("Genitiv", blank=True)
    neutral_dative = models.CharField("Dativ", blank=True)
    neutral_accusative = models.CharField("Akkusativ", blank=True)
    neutral_instrumental = models.CharField("Instrumental", blank=True)
    neutral_prepositive = models.CharField("Präpositiv", blank=True)

    singular_nominative = models.CharField("Nominativ", blank=True)
    singular_genitive = models.CharField("Genitiv", blank=True)
    singular_dative = models.CharField("Dativ", blank=True)
    singular_accusative = models.CharField("Akkusativ", blank=True)
    singular_instrumental = models.CharField("Instrumental", blank=True)
    singular_prepositive = models.CharField("Präpositiv", blank=True)

    plural_nominative = models.CharField("Nominativ", blank=True)
    plural_genitive = models.CharField("Genitiv", blank=True)
    plural_dative = models.CharField("Dativ", blank=True)
    plural_accusative = models.CharField("Akkusativ", blank=True)
    plural_instrumental = models.CharField("Instrumental", blank=True)
    plural_prepositive = models.CharField("Präpositiv", blank=True)

    class Meta:
        app_label = "words"
        verbose_name = "Pronomen Formen"
        verbose_name_plural = "Pronomen Formen"

    def get_fields(self):
        return [
            (field.verbose_name, getattr(self, field.name))
            for field in PronounInflection._meta.fields
        ]


class SubstantiveInflection(Inflection):
    partitive = models.CharField("Partitiv", blank=True)
    locative = models.CharField("Lokativ", blank=True)

    singular_nominative = models.CharField("Nominativ", blank=True)
    singular_genitive = models.CharField("Genitiv", blank=True)
    singular_dative = models.CharField("Dativ", blank=True)
    singular_accusative = models.CharField("Akkusativ", blank=True)
    singular_instrumental = models.CharField("Instrumental", blank=True)
    singular_prepositive = models.CharField("Präpositiv", blank=True)

    plural_nominative = models.CharField("Nominativ", blank=True)
    plural_genitive = models.CharField("Genitiv", blank=True)
    plural_dative = models.CharField("Dativ", blank=True)
    plural_accusative = models.CharField("Akkusativ", blank=True)
    plural_instrumental = models.CharField("Instrumental", blank=True)
    plural_prepositive = models.CharField("Präpositiv", blank=True)

    class Meta:
        app_label = "words"
        verbose_name = "Substantiv Formen"
        verbose_name_plural = "Substantiv Formen"

    def get_fields(self):
        return [
            (field.verbose_name, getattr(self, field.name))
            for field in SubstantiveInflection._meta.fields
        ]


class VerbInflection(Inflection):
    present_singular_1 = models.CharField("я", blank=True)
    present_singular_2 = models.CharField("ты", blank=True)
    present_singular_3 = models.CharField("он/она", blank=True)
    present_plural_1 = models.CharField("мы", blank=True)
    present_plural_2 = models.CharField("вы", blank=True)
    present_plural_3 = models.CharField("они", blank=True)

    future_singular_1 = models.CharField("я", blank=True)
    future_singular_2 = models.CharField("ты", blank=True)
    future_singular_3 = models.CharField("он/они", blank=True)
    future_plural_1 = models.CharField("мы", blank=True)
    future_plural_2 = models.CharField("вы", blank=True)
    future_plural_3 = models.CharField("они", blank=True)

    past_masculine = models.CharField("Maskulinum", blank=True)
    past_feminine = models.CharField("Femininum", blank=True)
    past_neutral = models.CharField("Neutrum", blank=True)
    past_plural = models.CharField("Plural", blank=True)

    participle_active_present = models.CharField("Präsens Aktiv", blank=True)
    participle_active_past = models.CharField("Präteritum Aktiv", blank=True)

    participle_passive_present = models.CharField("Präsens Passiv", blank=True)
    participle_passive_past = models.CharField("Präteritum Passiv", blank=True)

    participle_adverbial_present = models.CharField("Präsens", blank=True)
    participle_adverbial_past = models.CharField("Präteritum", blank=True)

    imperative_singular = models.CharField("Singular", blank=True)
    imperative_plural = models.CharField("Plural", blank=True)

    class Meta:
        app_label = "words"
        verbose_name = "Verb Formen"
        verbose_name_plural = "Verb Formen"

    def get_fields(self):
        return [
            (field.verbose_name, getattr(self, field.name))
            for field in VerbInflection._meta.fields
        ]
