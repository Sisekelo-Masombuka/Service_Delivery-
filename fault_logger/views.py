from django.shortcuts import render


def report_fault_view(request):
    return render(request, "fault_logger/report_form.html")
