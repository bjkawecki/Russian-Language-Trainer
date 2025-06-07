from django import forms

from apps.shared.validators import cyrillic_validator


class ReviewForm(forms.Form):
    card_word_name = forms.CharField(
        label="Übersetzung", max_length=50, validators=[cyrillic_validator]
    )
