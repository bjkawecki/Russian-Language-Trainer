from django.urls import path

# from apps.users.services.stripe.views.stripe import (
#     create_checkout_session,
#     payment_cancelled,
#     product_page,
#     stripe_config,
#     stripe_webhook,
#     subscription_confirm,
# )
from apps.users.views.subscription import SubscribeView

urlpatterns = [
    # path("stripe-config/", stripe_config, name="stripe_config"),
    # path("create-checkout-session/", create_checkout_session, name="create_checkout_session"),
    # path("product-page/", product_page, name="product_page"),
    # path("payment-cancelled/", payment_cancelled, name="payment_cancelled"),
    # path("subscription-confirm/", subscription_confirm, name="subscription_confirm"),
    # path("webhook/", stripe_webhook),
    # path("subscriptions/", Subscriptions.as_view(), name="subscriptions"),
    path(
        "subscribe/", SubscribeView.as_view(), name="subscribe"
    ),  # Bestimmten Kurs abonnieren
]
