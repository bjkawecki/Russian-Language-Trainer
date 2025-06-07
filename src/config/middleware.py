from django.shortcuts import redirect
from config.settings.common import MAINTENANCE
from django.http import Http404
from django.utils.deprecation import MiddlewareMixin


class AuthRequiredMiddleware(MiddlewareMixin):
    def process_request(self, request):
        protected_paths = ["/feed/"]

        if request.path in protected_paths:
            if request.user.is_authenticated:
                return  # Zugriff erlaubt
            elif request.COOKIES.get("sessionid"):  # Nutzer hat abgelaufenes Token
                return redirect(f"/signin/?next={request.path}")
            else:
                raise Http404


class LoginRequiredMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (
            not request.user.is_authenticated
            and request.path != "/"
            and not request.path.startswith("/signin")
            and not request.path.startswith("/signup")
            and not request.path.startswith("/404")
            and not request.path.startswith("/maintenance")
            and not request.path.startswith("/account-reset-password")
            and not request.path.startswith("/datenschutzerklaerung")
            and not request.path.startswith("/agb")
            and not request.path.startswith("/impressum")
            and not request.path.startswith("/widerrufsbelehrung")
        ):
            return redirect("error_404")
        response = self.get_response(request)
        return response


class MaintenanceMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (
            MAINTENANCE
            and request.path != "/"
            and not request.path.startswith("/maintenance")
            and not request.path.startswith("/datenschutzerklaerung")
            and not request.path.startswith("/agb")
            and not request.path.startswith("/impressum")
            and not request.path.startswith("/widerrufsbelehrung")
        ):
            return redirect("maintenance")

        response = self.get_response(request)
        return response
