from django import forms

from apps.users.models import User


class ChangeDeckNameLanguageForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangeDeckNameLanguageForm, self).__init__(*args, **kwargs)
        self.initial["is_deck_name_russian"] = self.user.is_deck_name_russian

    class Meta:
        model = User
        fields = ["is_deck_name_russian"]


class ShowExamplesForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ShowExamplesForm, self).__init__(*args, **kwargs)
        self.initial["show_examples"] = self.user.show_examples

    class Meta:
        model = User
        fields = ["show_examples"]


class ChangeShowWelcomeModalForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangeShowWelcomeModalForm, self).__init__(*args, **kwargs)
        self.initial["show_welcome_modal"] = self.user.show_welcome_modal

    class Meta:
        model = User
        fields = ["show_welcome_modal"]


class ChangeUsernameForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangeUsernameForm, self).__init__(*args, **kwargs)
        self.initial["first_name"] = self.user.first_name
        self.initial["last_name"] = self.user.last_name

    password = None

    class Meta:
        model = User
        fields = ["first_name", "last_name"]


class ChangeMaxNewCardsForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangeMaxNewCardsForm, self).__init__(*args, **kwargs)
        self.initial["max_new_cards"] = self.user.max_new_cards

    password = None

    class Meta:
        model = User
        fields = [
            "max_new_cards",
        ]


class DeleteUserForm(forms.Form):
    confirm = forms.CharField(label="Bestätigen", max_length=7)

    def clean_confirm(self):
        confirm = self.cleaned_data.get("confirm")
        if confirm != "LÖSCHEN":
            raise forms.ValidationError("Falsche Eingabe.")


UNITS = (("Minute(n)"), ("Stunde(n)"), ("Tag(e)"))


class StepForm(forms.Form):
    step = forms.IntegerField(label="Lernschritte", required=True)
    unit = forms.ChoiceField(choices=UNITS)
