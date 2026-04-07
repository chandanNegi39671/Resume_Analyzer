from django.urls import path
from .views import analyze_resume

urlpatterns = [
    path("analyze/", analyze_resume,
    name="analyze"),
]