import socket

from dotenv import load_dotenv

from config.settings.subsettings.apps import (
    APPS,
    DEV_APPS,
    DJANGO_APPS,
    THIRD_PARTY_APPS,
)
from config.settings.subsettings.middleware import (
    CUSTOM_MIDDLEWARE,
    DEV_MIDDLEWARE,
    MIDDLEWARE,
)
from config.settings.utils import get_env_variable

load_dotenv()
STAGE = get_env_variable("STAGE", "False").lower() == "true"
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[:-1] + "1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]

INSTALLED_APPS = DJANGO_APPS + DEV_APPS + THIRD_PARTY_APPS + APPS

MIDDLEWARE = MIDDLEWARE + DEV_MIDDLEWARE + CUSTOM_MIDDLEWARE

CSRF_TRUSTED_ORIGINS = get_env_variable("CSRF_TRUSTED_ORIGINS").split(",")
CSRF_ALLOWED_ORIGINS = get_env_variable("CSRF_ALLOWED_ORIGINS").split(",")
CORS_ORIGINS_WHITELIST = get_env_variable("CORS_ORIGINS_WHITELIST").split(",")

FIRST_NAME = get_env_variable("FIRST_NAME")
LAST_NAME = get_env_variable("LAST_NAME")
EMAIL = get_env_variable("EMAIL")
NEW_PASSWORD = get_env_variable("NEW_PASSWORD")


def show_toolbar(request):
    return True


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": show_toolbar,
}
