from django.db.models import Q
from django.utils import timezone

from apps.announcements.models import Announcement, UserAnnouncement


class AnnouncementsMixin:
    """Handles the logic for showing the welcome modal."""

    def get_announcements(self, user, category=None, marked_as_read=None):
        announcement_filter = Q()
        if category:
            announcement_filter &= Q(announcement__category=category)
        if marked_as_read:
            announcement_filter &= Q(announcement__marked_as_read=marked_as_read)
        return UserAnnouncement.objects.filter(
            announcement_filter,
            announcement__is_active=True,
            user=user,
            announcement__starting_at__lte=timezone.now(),
        ).order_by("-announcement__starting_at")[:5]

    def get_category_choices(self):
        return {value: display for value, display in Announcement.Category.choices}
