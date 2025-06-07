from allauth.account.models import EmailAddress
from allauth.account.views import EmailView, PasswordChangeView
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView

from apps.courses.models import Course
from apps.users.forms.settings import (
    ChangeDeckNameLanguageForm,
    ChangeUsernameForm,
    DeleteUserForm,
    ShowExamplesForm,
    StepForm,
)
from apps.users.mixins.settings import SettingsMixin
from apps.users.services.deactivation import SettingsDeleteUserServices
from apps.users.services.steps import SettingsStepsServices
from apps.users.services.stripe import get_user_subscription
from config.settings.common import BETA


class CustomEmailView(LoginRequiredMixin, EmailView):
    template_name = "settings/custom-change-email.html"


class CustomPasswordChange(LoginRequiredMixin, PasswordChangeView):
    template_name = "settings/custom-change-password.html"

    success_url = reverse_lazy("settings")


class ChangeDeckNameLanguage(LoginRequiredMixin, UpdateView):
    template_name = "settings/change-deck-language.html"
    form_class = ChangeDeckNameLanguageForm
    success_url = reverse_lazy("settings")

    def get_form_kwargs(self):
        kwargs = super(ChangeDeckNameLanguage, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_object(self, queryset=None):
        return self.request.user


class DeleteUser(LoginRequiredMixin, TemplateView):
    form_class = DeleteUserForm
    template_name = "settings/delete-account.html"

    def post(self, request):
        form = self.form_class(request.POST)
        if not form.is_valid():
            return render(
                request, "settings/delete-account.html", context={"form": form}
            )
        user_email = request.user.email
        user = request.user
        email_obj = EmailAddress.objects.get(user=user, email=user_email)
        email_obj.verified = False
        email_obj.save()

        SettingsDeleteUserServices.send_deactivation_confirmation_email(user_email)
        logout(request)
        user.delete()
        messages.success(request, "Ihr Konto wurde gelöscht.")
        return redirect("signin")


class Settings(LoginRequiredMixin, TemplateView):
    template_name = "settings/overview.html"

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context["steps"] = SettingsStepsServices.get_steps_as_strings(user)
        if BETA:
            return context
        else:
            subscription = get_user_subscription(user)
            context["subscription"] = subscription
            context["user_courses"] = Course.objects.filter(user=user)
            return context


class ChangeShowExamples(LoginRequiredMixin, UpdateView):
    template_name = "settings/show-examples.html"
    form_class = ShowExamplesForm
    success_url = reverse_lazy("settings")

    def get_form_kwargs(self):
        kwargs = super(ChangeShowExamples, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_object(self, queryset=None):
        return self.request.user


class ChangeSteps(LoginRequiredMixin, TemplateView, SettingsMixin):
    template_name = "settings/change-steps.html"
    context_object_name = "steps"
    form_class = StepForm
    success_url = reverse_lazy("settings")

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        choices = ["Minute(n)", "Stunde(n)", "Tag(e)"]
        context["steps_units"] = SettingsStepsServices.get_steps(user)
        context["choices"] = choices
        return context

    def post(self, request, *args, **kwargs):
        context = {}
        user = self.request.user
        steps = self.request.POST.getlist("steps")
        steps = map(int, steps)
        units = self.request.POST.getlist("units")
        steps_as_minutes = self.convert_to_minutes(steps, units)
        SettingsStepsServices.save_steps(user, steps_as_minutes)
        context["steps"] = SettingsStepsServices.get_steps_as_strings(user)
        return redirect("settings")


class ChangeUsername(LoginRequiredMixin, UpdateView):
    template_name = "settings/change-username.html"
    form_class = ChangeUsernameForm
    success_url = reverse_lazy("settings")

    def get_form_kwargs(self):
        kwargs = super(ChangeUsername, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
