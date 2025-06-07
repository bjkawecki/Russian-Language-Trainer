import json
import logging
import time

from django.contrib import messages
from django.core.cache import cache
from django.http import StreamingHttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView

from apps.courses.models import Course
from apps.importer.forms import ImportCourseDataForm, ImportProverbDataForm
from apps.importer.mixins import LoadProverbsJSONMixin
from config.tasks import update_or_create_course_task

logger = logging.getLogger("django")


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


class ImportProverbData(LoadProverbsJSONMixin, FormView):
    form_class = ImportProverbDataForm
    success_url = reverse_lazy("data_import")
    template_name = "components/proverb/import-form.html"

    def form_valid(self, form):
        json_file = form.cleaned_data["proverbs_json_file"]
        try:
            success = self.save_proverbs_from_file(json_file)
            if success:
                messages.success(
                    self.request, "Liste mit Sprichwörtern wurde erfolgreich geladen."
                )
            else:
                messages.error(
                    self.request,
                    "Einige Sprichwörter konnten nicht verarbeitet werden. Überprüfen Sie die Datei.",
                )
        except Exception as e:
            messages.error(
                self.request,
                f"Ein unerwarteter Fehler ist aufgetreten: {str(e)}. Bitte versuchen Sie es erneut.",
            )
            # Optional: Logging des Fehlers
            logger.exception("Error while processing the proverbs JSON file.")

        return super().form_valid(form)

    def form_invalid(self, form):
        """Handle invalid form submission."""
        messages.error(
            self.request, "Das Formular enthält Fehler. Bitte korrigieren Sie diese."
        )
        return super().form_invalid(form)
