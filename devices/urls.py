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
    ),


    path(
        "devices/",
        views.DeviceListView.as_view(),
        name="device_list",
    ),
    path(
        "devices/new/",
        views.DeviceCreateView.as_view(),
        name="device_create",
    ),
    path(
        "devices/<int:pk>/edit/",
        views.DeviceUpdateView.as_view(),
        name="device_update",
    ),
    path(
        "devices/<int:pk>/delete/",
        views.DeviceDeleteView.as_view(),
        name="device_delete",
    ),


]
