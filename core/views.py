from django.shortcuts import render


def map_landing_view(request):
    return render(request, "core/map_landing.html")
