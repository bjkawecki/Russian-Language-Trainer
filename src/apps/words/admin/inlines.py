from django.contrib import admin
from polymorphic.admin import StackedPolymorphicInline

from apps.users.models import User
from apps.words.models.example import Example
from apps.words.models.feature import (
    AdjectiveFeature,
    NumeralFeature,
    PrepositionFeature,
    PronounFeature,
    SubstantiveFeature,
    VerbFeature,
)
from apps.words.models.inflection import (
    AdjectiveInflection,
    NumeralInflection,
    PronounInflection,
    SubstantiveInflection,
    VerbInflection,
)
from apps.words.models.translation import Translation
from apps.words.models.word import Feature, Inflection


class ExampleInlines(admin.StackedInline):
    model = Example
    extra = 0


class TranslationInlines(admin.TabularInline):
    model = Translation.words.through
    extra = 0


class UserInlines(admin.TabularInline):
    model = User.word_set.through
    extra = 0


class InflectionInlines(StackedPolymorphicInline):
    class AdjectiveInflectionInlines(StackedPolymorphicInline.Child):
        model = AdjectiveInflection

    class NumeralInflectionInlines(StackedPolymorphicInline.Child):
        model = NumeralInflection

    class PronounInflectionInlines(StackedPolymorphicInline.Child):
        model = PronounInflection

    class SubstantiveInflectionInlines(StackedPolymorphicInline.Child):
        model = SubstantiveInflection

    class VerbInflectionInlines(StackedPolymorphicInline.Child):
        model = VerbInflection

    model = Inflection
    child_inlines = (
        AdjectiveInflectionInlines,
        NumeralInflectionInlines,
        PronounInflectionInlines,
        SubstantiveInflectionInlines,
        VerbInflectionInlines,
    )


class FeatureInlines(StackedPolymorphicInline):
    class AdjectiveFeatureInlines(StackedPolymorphicInline.Child):
        model = AdjectiveFeature

    class NumeralFeatureInlines(StackedPolymorphicInline.Child):
        model = NumeralFeature

    class PronounFeatureInlines(StackedPolymorphicInline.Child):
        model = PronounFeature

    class PrepositionFeatureInlines(StackedPolymorphicInline.Child):
        model = PrepositionFeature

    class SubstantiveFeatureInlines(StackedPolymorphicInline.Child):
        model = SubstantiveFeature

    class VerbFeatureInlines(StackedPolymorphicInline.Child):
        model = VerbFeature

    model = Feature
    child_inlines = (
        AdjectiveFeatureInlines,
        NumeralFeatureInlines,
        PrepositionFeatureInlines,
        PronounFeatureInlines,
        SubstantiveFeatureInlines,
        VerbFeatureInlines,
    )
