import json
import random

from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST


# Kimberley CBD — centre for Leaflet
MAP_CENTER = {"lat": -28.738, "lng": 24.763, "zoom": 13}

_INCIDENT_TYPES = [
    {"code": "P", "cls": "pin-pothole", "title": "Pothole"},
    {"code": "E", "cls": "pin-electricity", "title": "Electricity"},
    {"code": "W", "cls": "pin-water", "title": "Water"},
    {"code": "T", "cls": "pin-traffic", "title": "Traffic"},
    {"code": "S", "cls": "pin-streetlight", "title": "Streetlight"},
]


def _random_kimberley_incidents(n: int = 10):
    """
    Randomize incident pins within a small bounding box around Kimberley CBD.
    This keeps the demo looking 'on streets' without needing a geocoder.
    """
    # ~6–8km radius box around CBD (roughly)
    lat_min, lat_max = -28.780, -28.710
    lng_min, lng_max = 24.720, 24.820

    incidents = []
    for _ in range(n):
        t = random.choice(_INCIDENT_TYPES)
        incidents.append(
            {
                "code": t["code"],
                "cls": t["cls"],
                "title": t["title"],
                "lat": round(random.uniform(lat_min, lat_max), 6),
                "lng": round(random.uniform(lng_min, lng_max), 6),
            }
        )
    return incidents


def map_landing_view(request):
    ctx = {
        "map_center_json": json.dumps(MAP_CENTER),
        "map_incidents_json": json.dumps(_random_kimberley_incidents()),
    }
    return render(request, "core/map_landing.html", ctx)


def about_view(request):
    return render(request, "core/about.html")


def contact_view(request):
    return render(request, "core/contact.html")


@require_POST
def set_language_view(request):
    lang = request.POST.get("lang", "en")
    if lang in ("en", "af", "zu"):
        request.session["lang"] = lang
    next_url = request.POST.get("next") or "/"
    return redirect(next_url)
