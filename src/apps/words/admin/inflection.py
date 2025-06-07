from django.contrib import admin
from polymorphic.admin import PolymorphicChildModelAdmin, PolymorphicParentModelAdmin

from apps.words.models.inflection import (
    AdjectiveInflection,
    NumeralInflection,
    PronounInflection,
    SubstantiveInflection,
    VerbInflection,
)
from apps.words.models.word import Inflection


class InflectionChildAdmin(PolymorphicChildModelAdmin):
    base_model = Inflection
    list_per_page = 10


@admin.register(AdjectiveInflection)
class AdjectiveInflectionAdmin(InflectionChildAdmin):
    base_model = AdjectiveInflection
    show_in_index = False


@admin.register(NumeralInflection)
class NumeralInflectionAdmin(InflectionChildAdmin):
    base_model = NumeralInflection
    show_in_index = False


@admin.register(PronounInflection)
class PronounInflectionAdmin(InflectionChildAdmin):
    base_model = PronounInflection
    show_in_index = False


@admin.register(VerbInflection)
class VerbInflectionAdmin(InflectionChildAdmin):
    base_model = VerbInflection
    show_in_index = False


@admin.register(SubstantiveInflection)
class SubstantiveInflectionAdmin(InflectionChildAdmin):
    base_model = SubstantiveInflection
    show_in_index = False


@admin.register(Inflection)
class InflectionAdmin(PolymorphicParentModelAdmin):
    base_model = Inflection
    child_models = (
        AdjectiveInflection,
        NumeralInflection,
        PronounInflection,
        SubstantiveInflection,
        VerbInflection,
    )
    list_per_page = 10
