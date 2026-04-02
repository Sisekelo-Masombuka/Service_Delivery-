from django.urls import path

from .views import report_fault_view

urlpatterns = [
    path('report/', report_fault_view, name='report_fault'),
]
