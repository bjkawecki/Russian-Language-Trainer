import logging

from allauth.account.signals import email_confirmed, user_logged_in

from apps.announcements.models import Announcement, UserAnnouncement
from apps.users.models import Step
from config.settings.common import BETA

logger = logging.getLogger("django")


def handle_user_email_confirmation(signal, sender, email_address, **kwargs):
    user = email_address.user
    default_steps = [10, 1440, 8640]
    for step in default_steps:
        step, _ = Step.objects.get_or_create(step=step, user=user)
        step.save()
    user.save()
    try:
        welcome_announcement = Announcement.objects.get(title="Willkommen bei Bajkal")
        UserAnnouncement.objects.create(user=user, announcement=welcome_announcement)
        if BETA:
            beta_announcement = Announcement.objects.get(
                title="Hinweise zur Beta-Phase"
            )
            UserAnnouncement.objects.create(user=user, announcement=beta_announcement)
    except Announcement.DoesNotExist as e:
        logger.error(e)


def handle_user_logged_in(request, user, **kwargs):
    request.session["successfull_login"] = True


email_confirmed.connect(handle_user_email_confirmation)

user_logged_in.connect(handle_user_logged_in)
