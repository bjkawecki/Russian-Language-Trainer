from django.contrib import admin

from apps.announcements.models import Announcement, UserAnnouncement


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    fields = ("id", "title", "message", "category", "is_active", "starting_at")
    readonly_fields = ("id",)
    list_display = ["id", "title", "is_active", "category", "starting_at"]
    list_display_links = ["id", "title"]
    search_fields = ("title", "message")
    list_filter = ("category", "is_active", "starting_at")
    list_per_page = 10


@admin.register(UserAnnouncement)
class UserAnnouncementAdmin(admin.ModelAdmin):
    fields = ("id", "announcement", "user", "marked_as_read")
    readonly_fields = ("id",)
    list_display = ["id", "announcement", "user", "marked_as_read"]
    list_display_links = ["announcement"]
    list_filter = ("announcement", "user", "marked_as_read")
    list_per_page = 10
    actions = ("mark_as_read", "mark_as_unread")

    @admin.action(description="Als gelesen markieren")
    def mark_as_read(self, request, queryset):
        queryset.update(marked_as_read=True)

    @admin.action(description="Als nicht gelesen markieren")
    def mark_as_unread(self, request, queryset):
        queryset.update(marked_as_read=False)
