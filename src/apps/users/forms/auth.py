from allauth.account.forms import LoginForm, SignupForm
from django import forms

from apps.users.models import User


class LoginUserForm(LoginForm):
    class Meta:
        model = User
        fields = (
            "login_field",
            "password",
        )

    field_order = ["login_field", "password"]

    def __init__(self, *args, **kwargs):
        super(LoginUserForm, self).__init__(*args, **kwargs)
        self.fields["login_field"].widget.attrs["placeholder"] = "beispiel@mail.de"
        self.fields["password"].widget = forms.PasswordInput(
            attrs={"placeholder": "••••••••", "class": "bg-gray-50"}
        )

        for fieldname in ["login_field", "password"]:
            self.fields[fieldname].help_text = None

    def login(self, request, user):
        pass

    login_field = forms.EmailField(
        max_length=30, label="E-Mail", required=True, show_hidden_initial="Email"
    )
    password = forms.CharField(
        max_length=30, label="Passwort", required=True, widget=forms.PasswordInput
    )


class RegisterUserForm(SignupForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    field_order = ["email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["placeholder"] = "beispiel@mail.de"
        # self.fields["first_name"].widget.attrs["placeholder"] = "Kevin"
        # self.fields["last_name"].widget.attrs["placeholder"] = "Müller"
        self.fields["password1"].widget.attrs["placeholder"] = "Mindestens 8 Zeichen"
        self.fields["password2"].widget.attrs["placeholder"] = "Erneut eingeben"

        for fieldname in ["password1", "password2"]:
            self.fields[fieldname].help_text = None

    def signup(self, request, user):
        pass

    # first_name = forms.CharField(max_length=30, label="Vorname", required=True, empty_value="Vorname")
    # last_name = forms.CharField(max_length=30, label="Nachname", required=True)
    email = forms.EmailField(
        max_length=30, label="E-Mail", required=True, show_hidden_initial="Email"
    )
    password1 = forms.CharField(
        max_length=30, label="Passwort", required=True, widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        max_length=30,
        label="Passwort (wiederholen)",
        required=True,
        widget=forms.PasswordInput,
    )
