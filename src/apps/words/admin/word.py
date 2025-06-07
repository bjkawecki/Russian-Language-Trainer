from django.contrib import admin
from polymorphic.admin import PolymorphicInlineSupportMixin

from apps.words.admin.inlines import (
    ExampleInlines,
    FeatureInlines,
    InflectionInlines,
    TranslationInlines,
    UserInlines,
)
from apps.words.models.word import Word


@admin.register(Word)
class WordAdmin(PolymorphicInlineSupportMixin, admin.ModelAdmin):
    search_fields = ("unique_name", "lemma_accent", "wordclass", "transcription")

    def sound_display(self, item):
        return item.sound_display

    sound_display.short_description = "audio"
    sound_display.allow_tags = True
    list_per_page = 10
    readonly_fields = ("id",)
    list_display = (
        "unique_name",
        "lemma_accent",
        "transcription",
        "wordclass",
        "course",
        "deck",
    )
    list_display_links = ("lemma_accent",)
    list_filter = ("wordclass", "course")

    inlines = [
        UserInlines,
        FeatureInlines,
        InflectionInlines,
        ExampleInlines,
        TranslationInlines,
    ]

    def get_name(self, obj):
        return obj.audio

    get_name.admin_order_field = "Audio"  # Allows column order sorting
    get_name.short_description = "Audio"  # Renames column head
