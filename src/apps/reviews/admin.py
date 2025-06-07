from django.contrib import admin

from apps.reviews.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    fields = (
        "date",
        "user",
        "reviewed_cards",
        "initial_cards",
        "in_progress_cards",
        "mastered_cards",
        "failed_cards",
    )
    search_fields = ("user",)
    list_filter = ("date",)
    list_per_page = 10
