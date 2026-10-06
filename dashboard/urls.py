from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("remember_preference/", views.remember_preference, name="remember_preference"),
]
