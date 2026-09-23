# organizations/views.py
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


class OrganizationListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = "organizations.view_organization"
    raise_exception = True

    model = Organization
    template_name = "organizations/organization_list.html"
    context_object_name = "organizations"

    def get_queryset(self):
        return Organization.objects.filter(is_active=True)


class OrganizationPageContextMixin:
    def get_context_data(
        self, **kwargs
    ):
        context = super().get_context_data(
            **kwargs
        )

        context["organizations"] = (
            Organization.objects.filter(
                is_active=True
            )
        )

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
    SuccessMessageMixin,
    DeleteView,
):
    permission_required = (
        "organizations.delete_organization"
    )
    raise_exception = True

    model = Organization
    template_name = (
        "organizations/"
        "organization_confirm_delete.html"
    )
    success_url = reverse_lazy(
        "organizations:organization_list"
    )
    success_message = (
        "Organización eliminada correctamente."
    )