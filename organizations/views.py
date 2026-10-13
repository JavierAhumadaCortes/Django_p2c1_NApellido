# organizations/views.py
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DeleteView, ListView, UpdateView
from .models import Organization
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import OrganizationForm
from django.contrib import messages

from django.utils import timezone

ORDERING_MAP = {
    "name": "name",
    "-name": "-name",
    "created": "created_at",
    "-created": "-created_at",
}

ALLOWED_PAGE_SIZES = {5, 15, 30}


class OrganizationListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = "organizations.view_organization"
    raise_exception = True

    model = Organization
    template_name = "organizations/organization_list.html"
    context_object_name = "organizations"
    paginate_by = 15
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        params = self.request.GET.copy()
        params.pop("page", None)

        context["query_params"] = (params.urlencode())

        context["page_size"] = (
            self.request.session.get("organization_page_size",15,)
        )

        return context

    def get_paginate_by(self, queryset):
        raw_size = self.request.GET.get("page_size")

        if raw_size:
            try:
                selected_size = int(raw_size)
            except ValueError:
                selected_size = 15
            if selected_size in ALLOWED_PAGE_SIZES:
                self.request.session["organization_page_size"] = selected_size

        return self.request.session.get(
            "organization_page_size",
            15,
        )

    #def get_queryset(self):
    #    return Organization.objects.filter(deleted_at__isnull=True)
    def get_queryset(self):
        qs = Organization.objects.filter(
            # organization=self.request.user.profile.organization,
            # deleted_at__isnull=True,
        )
        q = self.request.GET.get("q", "").strip()
        status_param = self.request.GET.get("status", "").strip().upper()

        if q:
            qs = qs.filter(Q(name__icontains=q))

        if status_param in {"ACTIVE", "INACTIVE"}:
            qs = qs.filter(is_active=status_param == "ACTIVE")

        raw_order = self.request.GET.get("order", "name")
        ordering = ORDERING_MAP.get(raw_order, "name")

        return qs.order_by(ordering)




class OrganizationPageContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["organizations"] = Organization.objects.filter(deleted_at__isnull=True)

        context["open_modal"] = True

        return context


class OrganizationCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    SuccessMessageMixin,
    OrganizationPageContextMixin,
    CreateView,
):
    permission_required = "organizations.add_organization"
    raise_exception = True

    model = Organization
    form_class = OrganizationForm
    template_name = "organizations/organization_list.html"
    success_url = reverse_lazy("organizations:organization_list")
    success_message = "Organización creada correctamente."


class OrganizationUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    SuccessMessageMixin,
    OrganizationPageContextMixin,
    UpdateView,
):
    permission_required = "organizations.change_organization"
    raise_exception = True

    model = Organization
    form_class = OrganizationForm
    template_name = "organizations/organization_list.html"
    success_url = reverse_lazy("organizations:organization_list")
    success_message = "Organización actualizada correctamente."


class OrganizationDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView,
):
    permission_required = "organizations.delete_organization"
    raise_exception = True

    model = Organization
    template_name = "organizations/organization_confirm_delete.html"

    success_url = reverse_lazy("organizations:organization_list")

    def get_queryset(self):
        return Organization.objects.filter(deleted_at__isnull=True)

    def form_valid(self, form):
        self.object.deleted_at = timezone.now()
        self.object.save(update_fields=["deleted_at"])

        messages.success(self.request, "Organización desactivada correctamente.")

        return HttpResponseRedirect(self.get_success_url())
