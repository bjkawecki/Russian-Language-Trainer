from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class Faq(LoginRequiredMixin, TemplateView):
    template_name = "help.html"
