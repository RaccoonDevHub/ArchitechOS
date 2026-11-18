from django.urls import path

from . import views

app_name = "hardware"


urlpatterns = [
    path("", views.home, name="home"),
    path("module/<slug:module>/", views.select_module, name="select_module"),
]