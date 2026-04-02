from django.urls import path

from .views import map_landing_view

urlpatterns = [
    path('', map_landing_view, name='map_landing'),
]
