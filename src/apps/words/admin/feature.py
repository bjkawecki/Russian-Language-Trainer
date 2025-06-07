from django.contrib import admin
from polymorphic.admin import PolymorphicChildModelAdmin, PolymorphicParentModelAdmin

from apps.words.models.feature import (
    AdjectiveFeature,
    AdverbFeature,
    NumeralFeature,
    PrepositionFeature,
    PronounFeature,
    SubstantiveFeature,
    VerbFeature,
)
from apps.words.models.word import Feature


class FeatureChildAdmin(PolymorphicChildModelAdmin):
    base_model = Feature
    list_per_page = 10


@admin.register(AdjectiveFeature)
class AdjectiveFeatureAdmin(FeatureChildAdmin):
    base_model = AdjectiveFeature
    show_in_index = False


@admin.register(AdverbFeature)
class AdverbFeatureAdmin(FeatureChildAdmin):
    base_model = AdverbFeature
    show_in_index = False


@admin.register(NumeralFeature)
class NumeralFeatureAdmin(FeatureChildAdmin):
    base_model = NumeralFeature
    show_in_index = False


@admin.register(PrepositionFeature)
class PrepositionFeatureAdmin(FeatureChildAdmin):
    base_model = PrepositionFeature
    show_in_index = False


@admin.register(PronounFeature)
class PronounFeatureAdmin(FeatureChildAdmin):
    base_model = PronounFeature
    show_in_index = False


@admin.register(SubstantiveFeature)
class SubstantiveFeatureAdmin(FeatureChildAdmin):
    base_model = SubstantiveFeature
    show_in_index = False


@admin.register(VerbFeature)
class VerbFeatureAdmin(FeatureChildAdmin):
    base_model = VerbFeature
    show_in_index = False


@admin.register(Feature)
class FeatureAdmin(PolymorphicParentModelAdmin):
    base_model = Feature
    child_models = (
        AdjectiveFeature,
        AdverbFeature,
        NumeralFeature,
        PrepositionFeature,
        PronounFeature,
        SubstantiveFeature,
        VerbFeature,
    )
    list_per_page = 10
