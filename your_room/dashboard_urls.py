"""URLs for the staff dashboard  (your_room/dashboard_urls.py)"""
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import dashboard_views as v

urlpatterns = [
    path("", v.dashboard_home, name="dash-home"),
    path(
        "login/",
        LoginView.as_view(template_name="your_room/dashboard/login.html", next_page="dash-home"),
        name="dash-login",
    ),
    path("logout/", LogoutView.as_view(next_page="dash-login"), name="dash-logout"),
    path("<str:unit_type>/", v.unit_list, name="dash-list"),
    path("<str:unit_type>/add/", v.unit_edit, name="dash-add"),
    path("<str:unit_type>/<int:pk>/", v.unit_edit, name="dash-edit"),
    path("<str:unit_type>/<int:pk>/delete/", v.unit_delete, name="dash-delete"),
]
