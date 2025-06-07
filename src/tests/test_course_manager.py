from django.test import TestCase

from apps.cards.enums import CardState
from apps.cards.models import Card
from apps.courses.models import Course
from apps.decks.models import Deck
from apps.users.models import User
from apps.words.models.word import Word


class CourseManagerTest(TestCase):
    def setUp(self):
        # Erstelle einen Benutzer, der für die Tests verwendet wird
        self.user = User.objects.create(email="testuser@mail.de", password="password")

        # Erstelle Kurs-Objekte
        self.course = Course.objects.create(name="A1")

        # Erstelle Deck-Objekte
        self.deck = Deck.objects.create(name="Deck_1", course=self.course)

        # Erstelle Word-Objekte und ordne sie einem Kurs zu
        self.word1 = Word.objects.create(
            course=self.course,
            wordclass=Word.WordClass.ADJECTIVE,
            name="тест",
            name_accent="тест",
        )
        self.word2 = Word.objects.create(
            course=self.course,
            wordclass=Word.WordClass.ADJECTIVE,
            name="тестдва",
            name_accent="тестдва",
        )
        self.word3 = Word.objects.create(
            course=self.course,
            wordclass=Word.WordClass.ADJECTIVE,
            name="тесттри",
            name_accent="тесттри",
        )

        # Erstelle Usercards, um den Lernzustand zu testen
        self.card1 = Card.objects.create(
            user=self.user, word=self.word1, state=CardState.INITIAL
        )
        self.card2 = Card.objects.create(
            user=self.user, word=self.word2, state=CardState.IN_PROGRESS
        )
        self.card3 = Card.objects.create(
            user=self.user, word=self.word3, state=CardState.MASTERED
        )

    def test_count_cards_and_decks(self):
        # Verwende den CourseManager, um count_cards_and_decks zu testen
        result = Course.objects.count_cards_and_decks().get(pk=self.course.pk)

        # Überprüfe, ob die Aggregationen korrekt durchgeführt wurden
        self.assertEqual(result.all_cards, 3)  # 3 Wörter insgesamt
        self.assertEqual(result.all_decks, 1)  # 1 Deck
        self.assertEqual(result.initial_cards, 1)  # 1 Wort im Lernzustand INITIAL
        self.assertEqual(
            result.in_progress_cards, 1
        )  # 1 Wort im Lernzustand IN_PROGRESS
        self.assertEqual(result.mastered_cards, 1)  # 1 Wort im Lernzustand MASTERED

    def test_no_words_in_course(self):
        # Erstelle einen Kurs ohne Wörter
        course_without_words = Course.objects.create(name="A2")

        result = Course.objects.count_cards_and_decks().get(pk=course_without_words.pk)

        self.assertEqual(result.all_cards, 0)
        self.assertEqual(result.all_decks, 0)
        self.assertEqual(result.initial_cards, 0)
        self.assertEqual(result.in_progress_cards, 0)
        self.assertEqual(result.mastered_cards, 0)
