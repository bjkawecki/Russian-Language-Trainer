from django.views.generic import TemplateView


class Error404(TemplateView):
    template_name = "errors/404-noauth.html"  # Standard-Template

    def get_template_names(self):
        # Überprüfen, ob der Nutzer eingeloggt ist
        if self.request.user.is_authenticated:
            return ["errors/404-auth.html"]  # Template für eingeloggte Nutzer
        else:
            return ["errors/404-noauth.html"]  # Template für nicht eingeloggte Nutzer


class Error500(TemplateView):
    template_name = "errors/500.html"


class Maintenance(TemplateView):
    template_name = "errors/maintenance.html"

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault("status", 503)
        return super().render_to_response(context, **response_kwargs)
