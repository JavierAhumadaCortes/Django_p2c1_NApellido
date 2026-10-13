from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("remember_preference/", views.remember_preference, name="remember_preference"),
    path(
        "websocket-demo/",
        views.websocket_page,
        name="websocket_page",
    ),

    path(
        "test-websocket/",
        views.test_websocket,
        name="test_websocket",
    ),
]
