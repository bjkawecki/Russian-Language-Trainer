from django.contrib import admin

from apps.words.models.translation import Translation
from apps.words.models.word import Word


class InlineWords(admin.StackedInline):
    model = Word
    extra = 0


@admin.register(Translation)
class TranslationAdmin(admin.ModelAdmin):
    fields = ("id", "name", "words")
    readonly_fields = ("id",)
    list_display = ["name"]
    search_fields = ("name",)
    list_per_page = 10
