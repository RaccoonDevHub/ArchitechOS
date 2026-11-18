from django.http import Http404
from django.shortcuts import render

MODULES = {
"fiches": "Fiches",
"builder": "Builder",
"following": "Following",
}

def home(request):
    return render(
    request,
    "hardware/home.html",
    {"modules": MODULES, "active_module": "fiches"},
)

def select_module(request, module):
    if module not in MODULES:
        raise Http404("Module introuvable")
    return render(
    request,
    "hardware/partials/trieur.html",
    {"modules": MODULES, "active_module": module},
)

