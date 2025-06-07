from django.contrib import admin

from apps.proverbs.models import Proverb


@admin.register(Proverb)
class ProverbAdmin(admin.ModelAdmin):
    fields = ("proverb_id", "proverb", "translation", "explanation", "equivalent")
    readonly_fields = ("proverb_id",)
    list_display = ("proverb_id", "proverb", "translation")
    list_display_links = ("proverb",)
    list_per_page = 10
    search_fields = ("proverb", "translation")
