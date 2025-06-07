import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from apps.courses.models import Course
from apps.decks.models import Deck
from apps.users.models import User
from apps.words.models.word import Word


class CourseModelTest(TestCase):
    def test_create_course(self):
        """Testet das Erstellen eines Kurses."""
        course = Course.objects.create(name="A1")
        assert course.name == "A1"
        assert str(course) == "A1"

    def test_create_course_invalid_level(self):
        """Testet das Erstellen eines Kurses mit ungültigem Niveau."""
        with pytest.raises(ValidationError):
            course = Course.objects.create(name="Z9")  # Ungültiger Kurslevel
            course.full_clean()
            course.save()

    def test_add_user_to_course(self):
        """Testet das Hinzufügen von Nutzern zu einem Kurs."""

        # Erstelle Benutzer
        user1 = User.objects.create(email="user1@example.com", password="testpass")
        user2 = User.objects.create(email="user2@example.com", password="testpass")

        # Erstelle Kurs
        course = Course.objects.create(name="B2")
        # Füge Benutzer hinzu
        course.user.add(user1, user2)

        # Teste, ob die Benutzer hinzugefügt wurden
        assert course.user.count() == 2
        assert user1 in course.user.all()
        assert user2 in course.user.all()

    def test_upload_json_file(self):
        """Testet das Hochladen einer JSON-Datei zu einem Kurs."""
        json_content = b'{"key": "value"}'
        json_file = SimpleUploadedFile(
            "test.json", json_content, content_type="application/json"
        )

        # Erstelle Kurs mit JSON-Datei
        course = Course.objects.create(name="C1", json_file=json_file)

        # Teste, ob die Datei gespeichert wurde
        assert course.json_file.name.startswith("json/")
        assert course.json_file.read() == json_content

    def test_unique_course_name(self):
        """Testet, ob der Kursname eindeutig ist."""
        Course.objects.create(name="A1")
        with pytest.raises(Exception):
            # Versuch, einen Kurs mit dem gleichen Namen zu erstellen
            Course.objects.create(name="A1")  # Duplicate name


class CourseModelMethodsTest(TestCase):
    def setUp(self):
        # Erstelle einen User für das Testen
        self.user = User.objects.create(email="testuser@mail.de", password="testpass")
        # Erstelle einen Kurs für das Testen
        self.course = Course.objects.create(name=Course.CourseLevel.A1)
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

    def test_course_str_method(self):
        # Teste die __str__ Methode
        self.assertEqual(str(self.course), self.course.name)

    def test_get_absolute_url(self):
        # Erwarte, dass die URL korrekt ist
        expected_url = reverse("course_details", kwargs={"name": self.course.name})
        self.assertEqual(self.course.get_absolute_url(), expected_url)
