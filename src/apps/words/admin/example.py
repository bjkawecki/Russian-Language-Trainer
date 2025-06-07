from django.contrib import admin

from apps.words.models.example import Example


@admin.register(Example)
class ExampleAdmin(admin.ModelAdmin):
    fields = ("id", "word", "russian", "german")
    readonly_fields = ("id",)
    list_display = ["id", "word", "russian", "german"]
    search_fields = ("russian", "german")
    list_per_page = 10
