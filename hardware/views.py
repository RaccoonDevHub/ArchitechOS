from django.shortcuts import render

def home(request):
    return render(request, "hardware/home.html")