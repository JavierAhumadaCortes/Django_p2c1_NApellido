from django.contrib import admin
from .models import Organization, Department, Zone

class DepartmentInline(admin.TabularInline):
    model = Department
    extra = 0
    fields = ("name",)
    show_change_link = True

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
    inlines = [DepartmentInline]

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
    
    
    
# accounts/admin.py
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "employee_code",
        "organization",
        "department",
        "phone",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__email",
        "employee_code",
        "organization__name",
        "department__name",
    )

    list_filter = (
        "organization",
        "department",
    )

    ordering = (
        "organization__name",
        "user__username",
    )

    list_select_related = (
        "user",
        "organization",
        "department",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "deleted_at",
    )

    list_per_page = 25