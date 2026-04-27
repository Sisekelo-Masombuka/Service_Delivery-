from django.urls import path

from .views import download_fault_pdf, report_fault_view, track_fault_view

urlpatterns = [
    path("report/", report_fault_view, name="report_fault"),
    path("track/", track_fault_view, name="track_fault"),
    path("pdf/<str:code>/", download_fault_pdf, name="fault_pdf"),
]
