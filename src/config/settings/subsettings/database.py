import dj_database_url

from config.settings.common import DEBUG
from config.settings.utils import get_env_variable

# --------------------------------------------------------------
# LOCAL DATABASE
# --------------------------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": get_env_variable("DB_NAME"),
        "USER": get_env_variable("DB_USER"),
        "PASSWORD": get_env_variable("DB_PASSWORD"),
        "HOST": get_env_variable("DB_HOST"),
        # "HOST": get_env_variable("localhost"),
        "PORT": int(get_env_variable("DB_PORT", "5432")),
    }
}

if DEBUG is False:
    DATABASE_URL = get_env_variable("DB_URL")
    DATABASES["default"] = dj_database_url.parse(DATABASE_URL)


# --------------------------------------------------------------
# AWS DATABASE
# --------------------------------------------------------------

# DATABASES = {
#     "default": {
#         "ENGINE": get_env_variable("DB_ENGINE", "django.db.backends.postgresql"),
#         "NAME": "bajkal_db_1",
#         "USER": "bajkal",
#         "PASSWORD": "Z|<YB[,b-B>%2TG`1=LF\?TF<Ix9Ei",
#         "HOST": "bajkal-database-1.cjae08sqkmrr.eu-central-1.rds.amazonaws.com",
#         "PORT": get_env_variable("DB_PORT", "5432"),
#     }
# }
