from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView

from apps.announcements.mixins import AnnouncementsMixin
from apps.announcements.models import UserAnnouncement


class Announcements(LoginRequiredMixin, AnnouncementsMixin, ListView):
    template_name = "announcement.html"
    model = UserAnnouncement
    context_object_name = "announcements"

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        UserAnnouncement.objects.filter(marked_as_read=False, user=user).update(
            marked_as_read=True
        )
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()

        category_filter = self.request.GET.get("category_option", None)
        user = self.request.user
        queryset = self.get_announcements(user, category_filter)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_filter = self.request.GET.getlist("filter", [])
        context["categories"] = self.get_category_choices()
        context["category_filter"] = category_filter
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.htmx:
            return render(self.request, "components/announcement-list.html", context)
        return super().render_to_response(context, **response_kwargs)
