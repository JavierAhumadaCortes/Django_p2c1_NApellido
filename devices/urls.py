from django.urls import path
from . import views

app_name = "devices"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("dispositivos/", views.catalogo, name="catalogo"),
    path(
        "zonas/<int:zona_id>/dispositivos/",
        views.dispositivos_zona,
        name="por_zona",
    ),
    path(
        "lista-dispositivos/",
        views.device_list,
        name="list",
    ),
    path(
        "remember_page_size",
        views.remember_page_size,
        name="remember_page_size"
    )
]
