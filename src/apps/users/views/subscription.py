import logging
import time

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.db import transaction
from django.http import StreamingHttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView, TemplateView
from djstripe.models import Customer, Product, Subscription

from apps.cards.models import Card
from apps.courses.models import Course
from apps.decks.models import Deck
from apps.users.services.stripe import subscribe_course
from apps.words.models.word import Word
from config.settings.common import BETA
from config.settings.utils import get_env_variable

logger = logging.getLogger("django")


class SubscribeView(LoginRequiredMixin, View):
    def post(self, request, course_id=None):
        user = request.user
        course_id = request.POST.get("course_id")  # Holt die course_id vom Button

        # Startet eine Datenbanktransaktion, um Konsistenz zu gewährleisten
        with transaction.atomic():
            try:
                # Wenn course_id angegeben ist, nur diesen Kurs verwenden, sonst alle Kurse
                if course_id:
                    course = get_object_or_404(Course, id=course_id)

                    course.user.add(user)
                    logger.info(f"User {user} subscribed to course {course}.")
                    logger.info(f"Synchronizing collections for user {user}.")

                    words = Word.objects.filter(course=course)
                    decks = Deck.objects.filter(course=course)

                    for deck in decks:
                        deck.user.add(user)

                    for word in words:
                        word.user.add(user)
                        logger.info(f"Creating usercards for user {user}.")
                        Card.objects.get_or_create(word=word, user=user)

                logger.info(f"Synchronizing for user {user} is done.")
                messages.success(request, "Abonnement erfolgreich.")
                return redirect("course_list")

            except (Course.DoesNotExist, Word.DoesNotExist) as e:
                logger.error(f"Abonnieren gescheitert. Fehler: {e}")
                messages.error(request, "Fehler. Versuchen Sie es später erneut.")
                return redirect("course_list")


def subscribe(request):
    user = request.user
    try:
        courses = Course.objects.all()
        for course in courses:
            course.user.add(user)
            if course:
                logger.info(f"User {user} subscribed to course {course}.")
                logger.info(f"Synchronizing collections for user {user}.")
                words = Word.objects.filter(course=course)
                decks = Deck.objects.filter(course=course)
                for deck in decks:
                    deck.user.add(user)
                for word in words:
                    word.user.add(user)
                    logger.info(f"Creating usercards for user {user}.")
                    usercard, _ = Card.objects.get_or_create(word=word, user=user)
                logger.info(f"Synchronizing for user {user} is done.")
                messages.success(request, "Abonnement erfolgreich.")
        return redirect("subscriptions")
    except (Course.DoesNotExist, Word.DoesNotExist) as e:
        logger.error(f"Abonnieren gescheitert. Fehler: {e}")
        messages.error(request, "Fehler. Versuchen Sie es später erneut.")


class Subscriptions(TemplateView):
    template_name = "subscriptions.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if BETA is True:
            context["BETA"] = True
            context["course_a1_exists"] = Course.objects.filter().exists()
            context["courses"] = Course.objects.count_cards_and_decks()
            return context
        else:
            user = self.request.user
            try:
                subscription = Subscription.objects.get(user=user)
            except Subscription.DoesNotExist as e:
                logger.error(e)
                subscription = Subscription.objects.none()
            try:
                customer = Customer.objects.get(user=user)
            except Customer.DoesNotExist as e:
                logger.error(e)
                customer = Customer.objects.none()
            try:
                products = Product.objects.all().order_by("created")
                for product in products:
                    metadata = product.metadata
                    features = metadata.get("features")
                    extra_features = metadata.get("extra_features")
                    if features:
                        features = metadata["features"]
                        features = features.split(";")
                        product.feature_list = features
                    if extra_features:
                        extra_features = metadata["extra_features"]
                        extra_features = extra_features.split(";")
                        product.extra_feature_list = extra_features
                    for price in product.prices.filter(
                        product=product, recurring__interval="month"
                    ):
                        product.price_id = price.id

            except Product.DoesNotExist as e:
                logger.error(e)
                products = Product.objects.none()

            context["stripe_public_key"] = get_env_variable("STRIPE_PUBLISHABLE")
            context["stripe_pricing_table_id"] = get_env_variable(
                "STRIPE_PRICING_TABLE_ID"
            )
            context["subscription"] = subscription
            context["customer"] = customer
            context["products"] = products

            return context


# class SubscriptionView(ListView):
#     model = Course
#     template_name = "settings/subscription-settings.html"
#     context_object_name = "courses"

#     def get_queryset(self):
#         user = self.request.user
#         return subscription.get_courses(user)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         products = Product.objects.all().order_by("created")

#         for product in products:
#             features = product.metadata["features"]
#             features = features.split(";")
#             product.feature_list = features
#         context["products"] = products
#         return context


class CourseSubscribe(ListView):
    model = Course
    template_name = "settings/partials/subscription-list.html"
    context_object_name = "courses"

    def get_queryset(self):
        user = self.request.user
        name = self.kwargs["name"]
        return subscribe_course(name, user)


def subscription_update_stream(request):
    """
    Sends server-sent events to the client.
    """

    def event_stream():
        cache.set("subscription_progress", 0, timeout=10)
        while True:
            progress = cache.get("subscription_progress", "has expired")
            data = progress or 0
            yield "\ndata: {}\n\n".format(data)
            time.sleep(0.01)

    return StreamingHttpResponse(event_stream(), content_type="text/event-stream")


@login_required
def subscription_settings(request):
    if BETA:
        return render(request, "settings/no-subscription.html", {"BETA": BETA})
    else:
        user = request.user
        try:
            subscription = Subscription.objects.get(user=user)
        except Subscription.DoesNotExist as e:
            logger.error(e)
            subscription = Subscription.objects.none()
        try:
            customer = Customer.objects.get(user=user)
        except Customer.DoesNotExist as e:
            logger.error(e)
            customer = Customer.objects.none()
        try:
            products = Product.objects.all().order_by("created")
        except Product.DoesNotExist as e:
            logger.error(e)
            products = Product.objects.none()

        if subscription:
            return render(
                request,
                "settings/subscription-settings.html",
                {
                    "stripe_public_key": get_env_variable("STRIPE_PUBLISHABLE"),
                    "stripe_pricing_table_id": get_env_variable(
                        "STRIPE_PRICING_TABLE_ID"
                    ),
                    "subscription": subscription,
                    "customer": customer,
                    "products": products,
                },
            )
        else:
            return render(
                request,
                "settings/no-subscription.html",
                {
                    "stripe_public_key": get_env_variable("STRIPE_PUBLISHABLE"),
                    "stripe_pricing_table_id": get_env_variable(
                        "STRIPE_PRICING_TABLE_ID"
                    ),
                    "subscription": subscription,
                    "customer": customer,
                    "products": products,
                },
            )


def synchronize_userards(request):
    user = request.user
    try:
        courses = Course.objects.filter(user=user)
        words = Word.objects.filter(course__in=courses)
        logger.info(f"Start synchronizing usercards of user {user}...")
        if words:
            for word in words:
                usercard, _ = Card.objects.get_or_create(word=word, user=user)
            logger.info(f"Synchronizing usercards of user {user} is done.")
            messages.success(request, "Karten wurden synchronisiert.")
        else:
            messages.info(request, "Keine Karten vorhanden.")
        return redirect("subscription_settings")
    except (Course.DoesNotExist, Word.DoesNotExist) as e:
        logger.error(
            f"Synchronisieren der Karten von Nutzer {user} gescheitert. Fehler: {e}"
        )
        messages.error(request, "Fehler. Versuchen Sie es später erneut.")
