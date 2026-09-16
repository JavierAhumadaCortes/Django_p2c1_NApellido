# devices/admin.py
from django.contrib import admin
from .models import Device

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "serial_number",
        "organization",
        "zone",
        "organization__is_active",
    )
    search_fields = (
        "name",
        "serial_number",
        "organization__name",
        "zone__name",
    )
    list_filter = ("organization", "zone", "organization__is_active")
    ordering = ("organization__name", "name")
    list_select_related = ("organization", "zone")