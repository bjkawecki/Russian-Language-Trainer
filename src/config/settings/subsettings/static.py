from config.settings.common import BASE_DIR


STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "django.contrib.staticfiles.finders.FileSystemFinder",
)

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

STATIC_URL = "/static/"
STATIC_ROOT = "/volume/staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = "/volume/mediafiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",  # ✅ Nur zusätzliche statische Quellen
]
