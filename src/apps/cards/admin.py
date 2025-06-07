from django.contrib import admin

from apps.cards.enums import CardState
from apps.cards.models import Card


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    fields = ("id", "user", "word", "state", "ease", "interval", "due_date")
    readonly_fields = ("id", "due_date")
    list_display = ("word", "user", "state", "ease", "interval")
    list_display_links = ("word",)
    list_per_page = 10
    search_fields = ("word", "user")
    list_filter = ("state", "ease", "interval", "due_date")
    actions = ("reset_cards_state",)

    @admin.display(description="Stapel", ordering="deck__name")
    def get_deck_name(self, obj):
        return obj.word.deck.name

    @admin.display(description="Kurs")
    def get_course_name(self, obj):
        return obj.word.course.name

    @admin.action(description="Status aller Karten zurücksetzen.")
    def reset_cards_state(self, request, queryset):
        queryset.update(state=CardState.INITIAL)
