from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from apps.support.forms import UserMessageForm
from apps.support.mixins import UserMessageTopicsMixin
from apps.support.models import UserMessage


class UserMessageView(LoginRequiredMixin, CreateView, UserMessageTopicsMixin):
    model = UserMessage
    template_name = "contact.html"
    form_class = UserMessageForm
    success_url = reverse_lazy("message")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["user_messages"] = UserMessage.objects.filter(user=user)
        context["message_form_topics"] = self.get_topics()
        return context

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        messages.success(self.request, "Nachricht wurde gesendet.")
        return super().form_valid(form)
