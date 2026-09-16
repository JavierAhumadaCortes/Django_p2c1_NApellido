# devices/admin.py
from django.contrib import admin
from .models import Device, Measurement, AlertRule


admin.site.register(AlertRule)

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
    

@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = (
        "device",
        "energy_kwh",
        "measured_at",
        "created_at",
    )
    search_fields = (
        "device__name",
        "device__serial_number",
    )
    list_filter = ("device__organization",)
    ordering = ("-measured_at",)
    date_hierarchy = "measured_at"
    list_select_related = (
        "device",
        "device__organization",
    )
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 50
