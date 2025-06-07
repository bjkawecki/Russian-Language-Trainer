DJANGO_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.postgres",
    "django.contrib.staticfiles",
]

DEV_APPS = [
    "debug_toolbar",
    "nplusone.ext.django",
]

THIRD_PARTY_APPS = [
    "django_cleanup.apps.CleanupConfig",
    "django_use_email_as_username.apps.DjangoUseEmailAsUsernameConfig",
    "django_extensions",
    "django_htmx",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "djstripe",
    "polymorphic",
    "django_celery_beat",
]

APPS = [
    "apps.announcements",
    "apps.cards",
    "apps.courses",
    "apps.decks",
    "apps.feed",
    "apps.importer",
    "apps.proverbs",
    "apps.reviews",
    "apps.shared",
    "apps.support",
    "apps.users",
    "apps.words",
    "config",
]
