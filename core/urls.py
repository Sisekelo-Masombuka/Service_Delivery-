from django.urls import path

from .views import about_view, contact_view, map_landing_view, set_language_view

urlpatterns = [
    path("", map_landing_view, name="map_landing"),
    path("about/", about_view, name="about"),
    path("contact/", contact_view, name="contact"),
    path("set-language/", set_language_view, name="set_ui_language"),
]
