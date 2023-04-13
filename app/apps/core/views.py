from typing import Any

from django.http import HttpRequest, JsonResponse
from django.views.generic import TemplateView


def livez(request: HttpRequest) -> JsonResponse:
    return JsonResponse({"ok": True}, status=200)


def readyz(request: HttpRequest) -> JsonResponse:
    return JsonResponse({"ok": True}, status=200)


class DashboardView(TemplateView):
    template_name = "core/dashboard.html"

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context
