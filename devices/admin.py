# devices/admin.py
from django.contrib import admin
from .models import Device, Measurement, AlertRule
from core.admin_utils import get_user_organization


admin.site.register(AlertRule)


# devices/admin.py
from django.contrib import admin, messages
from django.utils import timezone

@admin.action(
    description="Archivar dispositivos seleccionados",
    permissions=["change"],
)
def archive_devices(modeladmin, request, queryset):
    updated = queryset.filter(
        deleted_at__isnull=True
    ).update(deleted_at=timezone.now())

    modeladmin.message_user(
        request,
        f"{updated} dispositivo(s) archivado(s).",
        level=messages.SUCCESS,
    )


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("name", "serial_number", "organization", "zone", "organization__is_active", )
    search_fields = ("name", "serial_number", "organization__name", "zone__name", )
    list_filter = ("organization", "zone", "organization__is_active")
    ordering = ("organization__name", "name")
    list_select_related = ("organization", "zone")
    
    actions = [archive_devices]
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.filter(deleted_at__isnull=True)

        if request.user.is_superuser:
            return qs

        organization = get_user_organization(request)
        return qs.filter(organization=organization)
    
    # devices/admin.py
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.organization = get_user_organization(request)

        super().save_model(request, obj, form, change)

    # devices/admin.py
    def has_change_permission(self, request, obj=None):
        allowed = super().has_change_permission(request, obj)
        if not allowed:
            return False

        if obj is None or request.user.is_superuser:
            return True

        organization = get_user_organization(request)
        return obj.organization_id == organization.id



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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "device" and not request.user.is_superuser:
            organization = get_user_organization(request)
            kwargs["queryset"] = Device.objects.filter(
                organization=organization,
                deleted_at__isnull=True,
            )

        return super().formfield_for_foreignkey(
            db_field, request, **kwargs
        )

