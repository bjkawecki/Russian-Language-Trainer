from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from config.settings.common import ADMIN_URL, DEBUG
from config.views import Error404, Error500, Maintenance

urlpatterns = [
    path(f"{ADMIN_URL}", admin.site.urls),
    path("404", Error404.as_view(), name="error_404"),
    path("500", Error500.as_view(), name="error_500"),
    path("maintenance", Maintenance.as_view(), name="maintenance"),
    path("", include("apps.announcements.urls")),
    path("", include("apps.cards.urls")),
    path("", include("apps.courses.urls")),
    path("", include("apps.decks.urls")),
    path("", include("apps.feed.urls")),
    path("", include("apps.importer.urls")),
    path("", include("apps.reviews.urls")),
    path("", include("apps.support.urls")),
    path("", include("apps.users.urls.auth")),
    path("", include("apps.users.urls.private")),
    path("", include("apps.users.urls.public")),
    path("", include("apps.users.urls.settings")),
    path("", include("apps.users.urls.subscription")),
    path("accounts", include("allauth.urls")),
]
if DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns += debug_toolbar_urls()


admin.site.site_header = "Bajkal Administration"
admin.site.index_title = "Manage Russisch Trainer System"

handler404 = Error404.as_view()
