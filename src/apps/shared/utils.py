from django.utils.text import slugify


def custom_slugify(value):
    # Umlaute und ß ersetzen
    umlaut_map = {
        "ä": "ae",
        "ö": "oe",
        "ü": "ue",
        "Ä": "Ae",
        "Ö": "Oe",
        "Ü": "Ue",
        "ß": "ss",
    }
    for key, replacement in umlaut_map.items():
        value = value.replace(key, replacement)

    # Standard-Slugify anwenden
    return slugify(value)
