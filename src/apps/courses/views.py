import json
import time

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.core.paginator import EmptyPage, Paginator
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, ListView

from apps.courses.models import Course
from apps.decks.models import Deck
from apps.importer.forms import ImportCourseDataForm
from config.tasks import update_or_create_course_task


class CourseList(LoginRequiredMixin, ListView):
    model = Course
    template_name = "course-list/course-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["user_courses"] = Course.objects.filter(user=user)
        context["not_user_courses"] = Course.objects.exclude(user=user)

        return context


class CourseDetails(LoginRequiredMixin, DetailView):
    model = Deck
    template_name = "course-detail/course-detail.html"

    def get_object(self):
        user = self.request.user
        slug = self.kwargs["slug"]
        return (
            Course.objects.count_cards_and_decks(user=user)
            .prefetch_related("deck_set")
            .get(slug=slug, user=user)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        page_number = self.request.GET.get("page", 1)
        slug = self.kwargs["slug"]
        decks = (
            Deck.objects.count_cards(self.request.user)
            .select_related("course")
            .filter(course__slug=slug, user=user)
            .order_by("name")
        )
        paginator = Paginator(decks, 10)

        try:
            page_obj = paginator.page(page_number)
        except EmptyPage:
            page_obj = None

        # Hinzufügen der Seite zum Kontext
        context["page_obj"] = page_obj
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.htmx:
            return render(
                self.request, "course-detail/partials/deck-list.html", context
            )
        return super().render_to_response(context, **response_kwargs)


class AdminCourseList(ListView):
    model = Course
    template_name = "data-import.html"
    context_object_name = "courses"

    def get_queryset(self):
        return Course.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ImportCourseData(FormView):
    template_name = "components/course/import-form.html"
    form_class = ImportCourseDataForm
    success_url = reverse_lazy("data_import")

    def form_valid(self, form):
        json_file = form.cleaned_data["json_file"]
        successful = update_or_create_course_task(json_file)
        if successful:
            messages.success(self.request, "Der Kurs wurde erfolgreich angelegt.")
        return super(ImportCourseData, self).form_valid(form)


def import_course_stream(request):
    """
    Sends server-sent events to the client.
    """

    def event_stream():
        cache.set("course_progress", 0)
        while True:
            progress = cache.get("course_progress", "has expired")
            data_dict = {
                "course_progress": progress or 0,
            }
            data = json.dumps(data_dict)
            yield "\ndata: {}\n\n".format(data)
            time.sleep(0.1)

    return StreamingHttpResponse(event_stream(), content_type="text/event-stream")
