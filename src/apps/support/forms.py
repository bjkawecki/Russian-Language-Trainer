from django import forms

from apps.support.models import UserMessage


class UserMessageForm(forms.ModelForm):
    class Meta:
        model = UserMessage
        fields = ["topic", "title", "content"]
