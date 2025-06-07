from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

from apps.courses.models import Course
from apps.decks.models import Deck
from apps.reviews.models import Review
from apps.users.forms.user import UserCreationForm
from apps.users.models import Step, User
from apps.words.models.word import Word


class InlineCourses(admin.StackedInline):
    model = Course.user.through
    extra = 0


class InlineDecks(admin.StackedInline):
    model = Deck.user.through
    extra = 0


class InlineCards(admin.StackedInline):
    model = Word.user.through
    extra = 0


class InlineSteps(admin.StackedInline):
    model = Step
    extra = 0


class InlineReview(admin.StackedInline):
    model = Review
    extra = 0


class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    search_fields = ("email", "first_name", "last_name", "bajkal_customer_id")
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        # "subscription",
        # "customer",
    )
    readonly_fields = ["bajkal_customer_id", "id"]
    list_filter = ("is_staff", "is_active")
    list_per_page = 10
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    fieldsets = (
        (
            "Allgemein",
            {
                "fields": (
                    "email",
                    "password",
                    "first_name",
                    "last_name",
                    "bajkal_customer_id",
                    "id",
                    # "subscription",
                    # "customer",
                )
            },
        ),
        (
            "Einstellungen",
            {
                "fields": (
                    "daily_proverb",
                    "daily_proverb_updated",
                    "show_welcome_modal",
                    "is_deck_name_russian",
                    "show_examples",
                )
            },
        ),
        (
            "Erlaubnisse",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Datumsfelder", {"fields": ("last_login", "date_joined")}),
    )

    ordering = ("email",)
    inlines = [InlineDecks, InlineCourses, InlineSteps, InlineReview]


admin.site.register(User, CustomUserAdmin)
