from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = 'core'
urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("readyz", views.readyz, name="readyz"),
    path("livez", views.livez, name="livez"),
    path("favicon.ico", RedirectView.as_view(url='/static/favicon.ico')),
]
