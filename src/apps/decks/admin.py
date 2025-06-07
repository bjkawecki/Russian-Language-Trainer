from django.contrib import admin

from apps.decks.models import Deck
from apps.users.models import User
from apps.words.models.word import Word


class InlineWords(admin.StackedInline):
    model = Word
    extra = 0


class InlineUsers(admin.TabularInline):
    model = User.deck_set.through
    extra = 0


@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    fields = ("id", "name", "slug", "course", "user")
    readonly_fields = ("id",)
    list_per_page = 10
    list_display = ("name", "slug", "course")
    inlines = [InlineWords, InlineUsers]
    search_fields = ("name",)
    list_filter = ("course",)
    actions = ("update_slugs",)  # Registriert die benutzerdefinierte Aktion

    @admin.action(description="Aktualisiere Slugs für ausgewählte Objekte")
    def update_slugs(self, request, queryset):
        updated_count = 0
        for obj in queryset:
            old_slug = obj.slug
            obj.update_slug()  # Ruft die Methode im Modell auf
            if obj.slug != old_slug:
                updated_count += 1
