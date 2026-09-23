# organizations/urls.py
from django.urls import path
from .views import (
    OrganizationListView,
    OrganizationCreateView,
    OrganizationUpdateView,
    OrganizationDeleteView,
)

app_name = "organizations"

urlpatterns = [
    path(
        "",
        OrganizationListView.as_view(),
        name="organization_list",
    ),
    path(
        "new/",
        OrganizationCreateView.as_view(),
        name="organization_create",
    ),
    path(
        "<int:pk>/edit/",
        OrganizationUpdateView.as_view(),
        name="organization_update",
    ),
    path(
        "<int:pk>/delete/",
        OrganizationDeleteView.as_view(),
        name="organization_delete",
    ),
]