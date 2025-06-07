import logging

from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.courses.models import Course
from apps.users.models import Step
from config.settings.dev import FIRST_NAME, LAST_NAME, EMAIL, NEW_PASSWORD

User = get_user_model()

logger = logging.getLogger("django")


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        first_name = FIRST_NAME
        last_name = LAST_NAME
        email = EMAIL
        new_password = NEW_PASSWORD
        steps = [10, 1440, 8640]
        try:
            u = None

            if not User.objects.filter(is_superuser=True).exists():
                self.stdout.write("Superuser not found.")
                self.stdout.write("Creating new superuser...")
                u = User.objects.create_superuser(  # noqa: F841
                    email=email,
                    password=new_password,
                    first_name=first_name,
                    last_name=last_name,
                )
                self.stdout.write(f"Vorname:{first_name}")
                self.stdout.write(f"Nachname:{last_name}")
                self.stdout.write(f"Email: {email}")
                self.stdout.write(f"Password: {new_password}")
                self.stdout.write("Superuser created.")
                if u:
                    for step in steps:
                        step, _ = Step.objects.get_or_create(step=step, user=u)
                        step.save()

                    courses = Course.objects.all()
                    for course in courses:
                        if course:
                            course.user.add(u)

                    self.stdout.write("Creating new EmailAdress for superuser.")
                    email, created = EmailAddress.objects.get_or_create(
                        email=u.email, user=u, verified=True
                    )
                    if created:
                        self.stdout.write("EmailAdress for superuser created.")
            else:
                self.stdout.write("Superuser found. Skip creation.")
        except Exception as e:
            logger.error(e)
            self.stdout.write(f"There was an errer: {e}")
