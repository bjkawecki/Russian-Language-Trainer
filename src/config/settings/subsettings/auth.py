AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# --------------------------------------------------------------
# ALL_AUTH
# --------------------------------------------------------------

LOGIN_URL = "signin"
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_RATE_LIMITS = {"login_failed": "10/m/ip,5/5m/key"}
LOGIN_REDIRECT_URL = "/feed/"
LOGOUT_REDIRECT_URL = "/"
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_CHANGE_EMAIL = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = False
ACCOUNT_FORMS = {
    "signup": "apps.users.forms.auth.RegisterUserForm",
    # "change_password": "trainer.forms.password.ChangeUserPasswordForm",
    # "login": "trainer.forms.login.LoginUserForm",
}
FILTERS_DISABLE_HELP_TEXT = True
ACCOUNT_EMAIL_SUBJECT_PREFIX = ""
AUTH_USER_MODEL = "users.User"
