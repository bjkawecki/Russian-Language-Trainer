import logging

from django.core.cache import cache
from django.db.models import Count
from djstripe.models import Subscription

from apps.cards.models import Card
from apps.courses.models import Course
from apps.decks.models import Deck
from apps.users.models import User
from apps.words.models.word import Word

logger = logging.getLogger("django")


def get_user_subscription(user):
    try:
        subscription = Subscription.objects.get(user=user)
    except Subscription.DoesNotExist as e:
        logger.error(e)
        subscription = Subscription.objects.none()
    return subscription


logger = logging.getLogger("debug")


def get_courses(user):
    courses = Course.objects.annotate(
        quantity_of_cards=Count("word", distinct=True),
        quantity_of_decks=Count("deck", distinct=True),
    )
    course_obj = dict(
        (
            course,
            User.objects.filter(course=course, customer_id=user.customer_id).exists(),
        )
        for course in courses
    )
    return course_obj


def subscribe_course(name, user):
    course = Course.objects.get(name=name)
    decks = Deck.objects.filter(course=course)
    for deck in decks:
        deck.user.add(user)
    words = Word.objects.filter(course=course)

    for count, word in enumerate(words):
        word.user.add(user)
        usercard, _ = Card.objects.get_or_create(word=word, user=user)
        counter = count or 0
        progress = counter + 1
        cache.set("subscription_progress", progress, timeout=10)
    course.user.add(user)
    cache.delete("subscription_progress")
    return get_courses(user)
