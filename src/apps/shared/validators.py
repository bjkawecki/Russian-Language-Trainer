from django.core.validators import RegexValidator

CYRILLIC_ERROR_MESSAGE = (
    "Nur kyrillische Buchstaben, Satzzeichen und Leerzeichen erlaubt."
)
LATIN_ERROR_MESSAGE = "Nur lateinische Buchstaben, Satzzeichen und Leerzeichen erlaubt."

CYRILLIC_REGEX = (
    r"^[\u0401\u0451\u0410-\u044f.,:\–\- !?А́Е́И́О́У́Ы́Э́Ю́Я́áéи́óу́ы́э́я́ю́]*$"
    # Kyrillisch: Buchstaben, Satzzeichen, Leerzeichen und akzentuierte Zeichen
)

LATIN_REGEX = (
    r"^[a-zA-Z-äöüÄÖÜß.,:?!()– ']*$"
    # Lateinisch: Buchstaben (inkl. Umlaute), Satzzeichen, Leerzeichen und Bindestriche
)

cyrillic_validator = RegexValidator(CYRILLIC_REGEX, CYRILLIC_ERROR_MESSAGE)

latin_validator = RegexValidator(LATIN_REGEX, LATIN_ERROR_MESSAGE)
