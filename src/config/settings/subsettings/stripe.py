from config.settings.utils import get_env_variable

STRIPE_SECRET_KEY = get_env_variable("STRIPE_SECRET")
STRIPE_PUBLISHABLE = get_env_variable("STRIPE_PUBLISHABLE")
STRIPE_WEBHOOK_SECRET = get_env_variable("STRIPE_WEBHOOK_SECRET", None)
DJSTRIPE_WEBHOOK_SECRET = get_env_variable("DJSTRIPE_WEBHOOK_SECRET", "whsec_xxx")

STRIPE_LIVE_MODE = False
DJSTRIPE_FOREIGN_KEY_TO_FIELD = get_env_variable("DJSTRIPE_FOREIGN_KEY_TO_FIELD", "id")


STRIPE_TEST_PUBLIC_KEY = get_env_variable("STRIPE_PUBLISHABLE")
STRIPE_TEST_SECRET_KEY = get_env_variable("STRIPE_SECRET")
