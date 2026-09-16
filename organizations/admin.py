from django.contrib import admin
from .models import Organization, Department, Zone

#admin.site.register(Organization)
@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "tax_id",
        "is_active",
        "created_at",
    )
    search_fields = ("name", "tax_id")
    list_filter = ("is_active",)
    ordering = ("name",)
    list_per_page = 25

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "organization",
        "organization__is_active",
    )
    search_fields = (
        "name",
        "organization__name",
        "organization__tax_id",
    )
    list_filter = ("organization", "organization__is_active")
    ordering = ("organization__name", "name")
    list_select_related = ("organization",)

@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "organization__name",
        "created_at",
    )
    search_fields = ("name", "organization")
    list_filter = ("name","organization")
    ordering = ("name",)
    list_per_page = 25