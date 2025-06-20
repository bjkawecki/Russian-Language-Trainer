from django.contrib.auth.forms import UserCreationForm

from apps.users.models import User


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email",)
