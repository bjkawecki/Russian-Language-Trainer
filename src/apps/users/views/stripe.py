import logging

import stripe
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from djstripe.models import Subscription

from apps.cards.models import Card
from apps.courses.models import Course
from apps.words.models.word import Word
from config.settings.utils import get_env_variable

logger = logging.getLogger("django")


@csrf_exempt
def stripe_config(request):
    if request.method == "GET":
        stripe_config = {"publicKey": get_env_variable("STRIPE_PUBLISHABLE")}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    customer_email = request.user.email
    if request.method == "POST":
        price = request.GET.get("price", "")
        domain_url = get_env_variable("DOMAIN_URL")
        stripe.api_key = get_env_variable("STRIPE_SECRET_KEY")
        try:
            session = stripe.checkout.Session.create(
                ui_mode="embedded",
                client_reference_id=(
                    request.user.customer if request.user.is_authenticated else None
                ),
                # success_url=domain_url + "subscription-confirm?session_id={CHECKOUT_SESSION_ID}",
                # cancel_url=domain_url + "payment-cancelled/",
                return_url=domain_url + "/return?session_id={CHECKOUT_SESSION_ID}",
                payment_method_types=["word", "paypal", "sepa_debit"],
                customer_email=customer_email,
                mode="subscription",
                billing_address_collection="required",
                line_items=[
                    {
                        "price": price,
                        "quantity": 1,
                    }
                ],
            )
            # return JsonResponse({"sessionId": checkout_session["id"]})
            return JsonResponse({"clientSecret": session.client_secret})
        except Exception as e:
            return JsonResponse({"error": str(e)})


@login_required
def product_page(request):
    return render(request, "payment/product-page.html")


@login_required
def payment_cancelled(request):
    messages.info(request, ("Bezahlvorgang abgebrochen"))
    return redirect("subscriptions")


@login_required
def subscription_confirm(request):
    # set our stripe keys up
    stripe.api_key = get_env_variable("STRIPE_SECRET_KEY")
    user = request.user

    # get the session id from the URL and retrieve the session object from Stripe
    session_id = request.GET.get("session_id")
    session = stripe.checkout.Session.retrieve(session_id)

    # get the subscribing user from the client_reference_id we passed in above
    # client_reference_id = int(session.client_reference_id)
    # subscription_holder = get_user_model().objects.get(id=client_reference_id)
    # subscription_holder = get_user_model().objects.get(customer__id=client_reference_id)
    # sanity check that the logged in user is the one being updated
    # assert subscription_holder == request.user

    # get the subscription object form Stripe and sync to djstripe
    subscription = stripe.Subscription.retrieve(session.subscription)

    djstripe_subscription = Subscription.sync_from_stripe_data(
        subscription, api_key=stripe.api_key
    )

    product = stripe.Product.retrieve(subscription.plan.product)
    name = int(product.metadata.course_name)

    # set the subscription and customer on our user
    user.subscription = djstripe_subscription
    user.customer = djstripe_subscription.customer
    user.save()

    try:
        course = Course.objects.get(publ_id=name)
    except Course.DoesNotExist as e:
        logger.error(e)
        logger(f"Kurs mit öffentlicher ID {name} nicht gefunden.")
        messages.error(request, "Abonnement wurde nicht abgeschlossen.")
        return HttpResponseRedirect(reverse("subscription_settings"))

    words = Word.objects.filter(course=course)

    for word in words:
        usercard, _ = Card.objects.get_or_create(word=word, user=user)
    course.user.add(user)

    messages.success(request, "Abonnement wurde abgeschlossen.")
    return HttpResponseRedirect(reverse("subscription_settings"))


@login_required
@require_POST
def create_portal_session(request):
    stripe.api_key = get_env_variable("STRIPE_SECRET_KEY")
    portal_session = stripe.billing_portal.Session.create(
        customer=request.user.customer.id,
        return_url="http://localhost:8001/settings/subscription/",
    )
    return HttpResponseRedirect(portal_session.url)


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = get_env_variable("STRIPE_SECRET_KEY")
    endpoint_secret = get_env_variable("STRIPE_WEBHOOK_SECRET")
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        # Invalid payload
        logger.error(e)
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        logger.error(e)
        return HttpResponse(status=400)

    if event["type"] == "customer.subscription.deleted":
        session = event["data"]["object"]

        # get the session id from the URL and retrieve the session object from Stripe
        customer_id = session.customer
        subscription_holder = get_user_model().objects.get(customer__id=customer_id)
        # sanity check that the logged in user is the one being updated

        # assert subscription_holder == user

        # get the subscription object form Stripe and sync to djstripe
        stripe.api_key = get_env_variable("STRIPE_SECRET_KEY")
        subscription = stripe.Subscription.retrieve(
            session["items"]["data"][0]["subscription"]
        )
        djstripe_subscription = Subscription.sync_from_stripe_data(
            subscription, api_key=stripe.api_key
        )

        # set the subscription and customer on our user
        subscription_holder.subscription = djstripe_subscription
        subscription_holder.customer = djstripe_subscription.customer
        subscription_holder.save()

        courses = Course.objects.filter(user=subscription_holder)

        for course in courses:
            course.user.remove(subscription_holder)

    if event["type"] == "customer.subscription.updated":
        session = event["data"]["object"]

        # get the session id from the URL and retrieve the session object from Stripe
        customer_id = session.customer
        subscription_holder = get_user_model().objects.get(customer__id=customer_id)
        # sanity check that the logged in user is the one being updated

        # assert subscription_holder == user

        # get the subscription object form Stripe and sync to djstripe
        stripe.api_key = get_env_variable("STRIPE_SECRET_KEY")
        subscription = stripe.Subscription.retrieve(
            session["items"]["data"][0]["subscription"]
        )
        djstripe_subscription = Subscription.sync_from_stripe_data(
            subscription, api_key=stripe.api_key
        )

        # set the subscription and customer on our user
        subscription_holder.subscription = djstripe_subscription
        subscription_holder.customer = djstripe_subscription.customer
        subscription_holder.save()

    return HttpResponse(status=200)
