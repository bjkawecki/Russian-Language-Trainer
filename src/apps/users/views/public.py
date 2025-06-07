from allauth.account.views import LoginView, PasswordResetView, SignupView
from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from apps.users.models import User


class CustomPasswordResetView(PasswordResetView):
    template_name = "account/password_reset_custom.html"  # Dein eigenes Template

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            super().form_valid(
                form
            )  # Nur wenn die E-Mail existiert, wird die echte Reset-Mail gesendet

        # Immer die gleiche Erfolgsnachricht anzeigen, egal ob die E-Mail existiert oder nicht
        messages.info(
            self.request, "Überpüfen Sie Ihr E-Mail-Postfach für weitere Anweisungen."
        )
        return redirect("landingpage")


def logout_user(request):
    logout(request)
    messages.success(request, ("Abgemeldet. До встречи!"))
    return redirect("landingpage")


class LandingPage(TemplateView):
    template_name = "landingpage/landing.html"

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse("feed"))
        return super().get(request, *args, **kwargs)


class LoginPage(LoginView):
    template_name = "landingpage/signin.html"

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse("feed"))
        return super().get(request, *args, **kwargs)


class SignupPage(SignupView):
    template_name = "landingpage/signup.html"

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse("feed"))
        return super().get(request, *args, **kwargs)


class ImpressumView(TemplateView):
    template_name = "landingpage/policies/impressum.html"


class TermsView(TemplateView):
    template_name = "landingpage/policies/terms.html"


class CancellationView(TemplateView):
    template_name = "landingpage/policies/cancellation.html"


class PrivacyView(TemplateView):
    template_name = "landingpage/policies/privacy.html"
