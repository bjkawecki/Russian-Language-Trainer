from django.urls import path

# from apps.users.views.subscriptions import (
#     CourseSubscribe,
#     subscription_settings,
#     subscription_update_stream,
#     synchronize_userards,
# )
from apps.users.views.settings import (
    ChangeDeckNameLanguage,
    ChangeSteps,
    ChangeUsername,
    # ChangeShowExamples,
    CustomEmailView,
    CustomPasswordChange,
    DeleteUser,
    Settings,
)

urlpatterns = [
    path("settings/", Settings.as_view(), name="settings"),
    path("settings/change-email/", CustomEmailView.as_view(), name="change_email"),
    # path("settings/show-examples/", ChangeShowExamples.as_view(), name="change_show_examples"),
    path(
        "settings/change-deck-name-language/",
        ChangeDeckNameLanguage.as_view(),
        name="change_deck_name_language",
    ),
    path(
        "settings/change-password/",
        CustomPasswordChange.as_view(),
        name="change_password",
    ),
    path("settings/change-username/", ChangeUsername.as_view(), name="change_username"),
    path("settings/delete-account/", DeleteUser.as_view(), name="delete_account"),
    path("settings/change-steps/", ChangeSteps.as_view(), name="change_steps"),
    # path("settings/subscription/", subscription_settings, name="subscription_settings"),
    # path("settings/change-subscription/stream/", subscription_update_stream, name="subscription_update_stream"),
    # path("settings/<str:name>/subscribe/", CourseSubscribe.as_view(), name="subscribe_course"),
    # path("settings/synchronize-usercards/", synchronize_userards, name="synchronize_usercards"),
]
