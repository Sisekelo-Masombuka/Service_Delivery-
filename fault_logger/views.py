from urllib.parse import urlencode

from django.contrib import messages
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render
from django.urls import reverse

from core.i18n_messages import MESSAGES

from .forms import FaultReportForm
from .models import FaultReport
from .pdf_export import build_fault_pdf
from .utils import generate_tracking_code


def _issue_choices(L):
    return [
        (FaultReport.ISSUE_POTHOLE, L["issue_pothole"]),
        (FaultReport.ISSUE_WATER, L["issue_water"]),
        (FaultReport.ISSUE_STREETLIGHT, L["issue_streetlight"]),
        (FaultReport.ISSUE_ELECTRICITY, L["issue_electricity"]),
        (FaultReport.ISSUE_TRAFFIC, L["issue_traffic"]),
    ]


def report_fault_view(request):
    lang = request.session.get("lang", "en")
    L = MESSAGES.get(lang, MESSAGES["en"])
    translated = _issue_choices(L)

    initial = {}
    lat = request.GET.get("lat")
    lng = request.GET.get("lng")
    if lat and lng:
        try:
            initial["latitude"] = float(lat)
            initial["longitude"] = float(lng)
        except ValueError:
            pass
    if "latitude" not in initial:
        initial["latitude"] = -28.738
        initial["longitude"] = 24.763

    if request.method == "POST":
        form = FaultReportForm(
            request.POST,
            request.FILES,
            translated_choices=translated,
        )
        if form.is_valid():
            fault = form.save(commit=False)
            fault.tracking_code = generate_tracking_code()
            fault.save()
            dest = f"{reverse('track_fault')}?{urlencode({'code': fault.tracking_code, 'welcome': '1'})}"
            return redirect(dest)
        messages.error(request, "fix_form")
    else:
        form = FaultReportForm(initial=initial, translated_choices=translated)

    lat_val = form["latitude"].value()
    lng_val = form["longitude"].value()
    return render(
        request,
        "fault_logger/report_form.html",
        {
            "form": form,
            "location_preview_lat": lat_val,
            "location_preview_lng": lng_val,
        },
    )


def track_fault_view(request):
    code_in = ""
    if request.method == "POST":
        code_in = (request.POST.get("code") or "").strip()
    else:
        code_in = (request.GET.get("code") or "").strip()

    fault = None
    lookup_display = ""
    if code_in:
        code_norm = code_in.upper().replace(" ", "")
        lookup_display = code_norm
        fault = FaultReport.objects.filter(tracking_code=code_norm).first()

    return render(
        request,
        "fault_logger/track.html",
        {
            "fault": fault,
            "lookup_code": lookup_display,
            "welcome": request.GET.get("welcome") == "1",
        },
    )


def download_fault_pdf(request, code):
    code_norm = code.upper().replace(" ", "")
    fault = FaultReport.objects.filter(tracking_code=code_norm).first()
    if fault is None:
        return HttpResponseNotFound("Unknown tracking code.")
    pdf = build_fault_pdf(fault)
    response = HttpResponse(pdf, content_type="application/pdf")
    safe = fault.tracking_code.replace("/", "-")
    response["Content-Disposition"] = f'attachment; filename="citymendersa-{safe}.pdf"'
    return response
