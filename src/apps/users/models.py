from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

from apps.proverbs.models import Proverb
from apps.users.managers import CustomUserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    # remove "default=random_id" in case of error "table not found"
    bajkal_customer_id = models.CharField(
        "Kundennummer", unique=True, editable=False, max_length=20, null=True
    )
    max_new_cards = models.SmallIntegerField("Maximale Anzahl neue Karten", default=5)
    # Multiplikator wird auf alle Überprüfungen angewandt für kleine Anpassungen.
    interval_modifier = models.IntegerField("Intervall-Modifikator", default=100)
    success_rate = models.IntegerField("Erfolgsrate", default=0)
    show_welcome_modal = models.BooleanField(
        "Willkommensnachricht anzeigen", default=True
    )
    is_deck_name_russian = models.BooleanField(
        "Stapelsprache auf Russisch", default=False
    )
    show_examples = models.BooleanField("Beispiele beim Lernen anzeigen", default=True)
    daily_proverb_updated = models.DateField(blank=True, null=True)
    daily_proverb = models.ForeignKey(
        Proverb, on_delete=models.DO_NOTHING, null=True, blank=True
    )

    # subscription = models.ForeignKey(
    #     "djstripe.Subscription",
    #     null=True,
    #     blank=True,
    #     on_delete=models.SET_NULL,
    #     help_text="The user's Stripe Subscription object, if it exists",
    # )
    # customer = models.ForeignKey(
    #     "djstripe.Customer",
    #     null=True,
    #     blank=True,
    #     on_delete=models.SET_NULL,
    #     help_text="The user's Stripe Customer object, if it exists",
    # )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def create_random_id(self):
        return str(get_random_string(8, allowed_chars="123456789"))

    def save(self, *args, **kwargs):
        if not self.bajkal_customer_id:
            self.bajkal_customer_id = self.create_random_id()
            while User.objects.filter(
                bajkal_customer_id=self.bajkal_customer_id
            ).exists():
                self.bajkal_customer_id = self.create_random_id()
        super(User, self).save(*args, **kwargs)

    def has_course(self):
        return self.course_set.exists()

    def get_user_courses(self):
        if self.course_set.exists():
            return self.course_set.all()
        else:
            return None

    def has_usercards(self):
        if self.card_set.exists():
            return True

    def user_decks(self):
        return self.deck_set.all()

    objects = CustomUserManager()

    class Meta:
        app_label = "users"
        verbose_name = "Nutzer"
        verbose_name_plural = "Nutzer"

    def full_name(self, obj):
        return "{} {}".format(obj.first_name, obj.last_name)

    def __str__(self):
        return self.email

    @property
    def is_admin(self):
        return False


class Step(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    step = models.IntegerField(default=10)

    class Meta:
        app_label = "users"
        verbose_name = "Schritt"
        verbose_name_plural = "Schritte"

    def __str__(self):
        return str(self.step)
