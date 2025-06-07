import socket
from pathlib import Path

from dotenv import load_dotenv

from config.settings.subsettings.apps import (
    DJANGO_APPS,
)
from config.settings.subsettings.middleware import MIDDLEWARE
from config.settings.utils import get_env_variable

load_dotenv()  # noqa : F821

VERSION_INFO = "v0.3.8"

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DEBUG = True

SITE_ID = 1

STRIPE_SECRET_KEY = get_env_variable("STRIPE_SECRET")
STRIPE_PUBLISHABLE = get_env_variable("STRIPE_PUBLISHABLE")
STRIPE_WEBHOOK_SECRET = get_env_variable("STRIPE_WEBHOOK_SECRET", None)
DJSTRIPE_WEBHOOK_SECRET = get_env_variable("DJSTRIPE_WEBHOOK_SECRET", "whsec_xxx")

STRIPE_LIVE_MODE = False
DJSTRIPE_FOREIGN_KEY_TO_FIELD = get_env_variable("DJSTRIPE_FOREIGN_KEY_TO_FIELD", "id")


STRIPE_TEST_PUBLIC_KEY = get_env_variable("STRIPE_PUBLISHABLE")
STRIPE_TEST_SECRET_KEY = get_env_variable("STRIPE_SECRET")

DATA_UPLOAD_MAX_NUMBER_FIELDS = 100000  # higher than the count of fields
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "core.asgi.application"
LANGUAGE_CODE = "de-de"
USE_TZ = True
TIME_ZONE = "Europe/Berlin"
USE_I18N = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
SUSPEND_SIGNALS = False


load_dotenv()
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[:-1] + "1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]


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
    "apps.reviews",
    "apps.shared",
    "apps.support",
    "apps.users",
    "apps.words",
    "config",
]

INSTALLED_APPS = DJANGO_APPS + APPS + THIRD_PARTY_APPS

MIDDLEWARE = MIDDLEWARE


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",  # Standard für Tests
        "NAME": BASE_DIR
        / "db.sqlite3",  # Der Pfad zur SQLite-Datei (für normale Nutzung, nicht Tests)
    }
}
