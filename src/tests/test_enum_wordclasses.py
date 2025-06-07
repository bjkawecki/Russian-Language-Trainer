from django.test import TestCase

from apps.shared.utils import CardsEnums


class CardsEnumsTest(TestCase):
    def setUp(self):
        # Diese Methode wird vor jedem Testfall ausgeführt.
        self.cards_enums = CardsEnums()

    def test_wordclasses(self):
        # Das erwartete Dictionary, das von der wordclasses-Methode zurückgegeben werden sollte.
        expected_result = {
            "adjective": "Adjektiv",
            "adverb": "Adverb",
            "compound": "Kompositum",
            "conjunction": "Konjunktion",
            "interjection": "Interjektion",
            "numeral": "Numerale",
            "particle": "Partikel",
            "phrase": "Ausdruck",
            "preposition": "Präposition",
            "pronoun": "Pronomen",
            "substantive": "Substantiv",
            "verb": "Verb",
        }

        # Aufruf der Methode wordclasses und Überprüfung des Ergebnisses
        self.assertEqual(self.cards_enums.wordclasses(), expected_result)
