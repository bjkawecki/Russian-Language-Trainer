from django.contrib import admin

from apps.support.models import UserMessage


@admin.register(UserMessage)
class UserMessageAdmin(admin.ModelAdmin):
    fields = ("id", "topic", "content", "title", "created_at", "user")
    readonly_fields = ["id", "created_at"]
    list_display = ["id", "user", "topic", "title", "created_at"]
    list_display_links = ["title"]
    search_fields = ("content", "title")
    list_filter = ("topic", "created_at")
    list_per_page = 10
