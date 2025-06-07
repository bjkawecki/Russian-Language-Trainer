from django.conf import settings
from django.utils import timezone

from apps.announcements.models import UserAnnouncement


def project_context(request):
    context = {
        "support-email": "kontakt@bajkal-app.de",
        "version_info": settings.VERSION_INFO,
    }

    return context


def navbar_context(request):
    user = request.user
    if user.is_authenticated:
        context = UserAnnouncement.objects.filter(
            marked_as_read=False,
            announcement__is_active=True,
            user=user,
            announcement__starting_at__lte=timezone.now(),
        ).order_by("-announcement__starting_at")[:5]
        unread_count = context.count()
        return {"announcements_context": context, "unread_count": unread_count}
    else:
        return {"announcements_context": [], "unread_count": 0}
