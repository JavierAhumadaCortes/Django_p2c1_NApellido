from django.shortcuts import redirect, render
from django.http import HttpResponse
from .services import cargar_dispositivos
from django.contrib.auth.decorators import (
    login_required,
    permission_required,
)
from devices.models import Measurement
from django.core.paginator import Paginator
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .models import Device


ALLOWED_PAGE_SIZES = {5, 15, 30}


def inicio(request):

    contexto = {
        "sistema": "EcoEnergy",
        "mensaje": "Monitoreo energético responsable",
        "asignatura": "Programación Back End",
    }

    return render(
        request,
        "dispositivos/inicio.html",
        contexto,
    )


def catalogo(request):
    dispositivos = cargar_dispositivos()
    activos = sum(1 for item in dispositivos if item["estado"] == "Activo")

    contexto = {
        "dispositivos": dispositivos,
        "total": len(dispositivos),
        "total_activos": activos,
    }

    return render(request, "dispositivos/catalogo.html", contexto)


def dispositivos_zona(request, zona_id):
    if zona_id != 3:
        return HttpResponse("Zona no encontrada", status=404)
    return HttpResponse(f"Dispositivos de la zona {zona_id}")


@login_required
@permission_required(
    "devices.view_measurement",
    raise_exception=True,
)
def measurement_list(request):
    profile = getattr(request.user, "profile", None)
    if profile is None:
        raise PermissionDenied("La cuenta no posee un perfil habilitado.") 
    
    organization = request.user.profile.organization
    measurements = Measurement.objects.filter(
        device__organization=organization,
        deleted_at__isnull=True,
    )
    return render(
        request,
        "measurements/list.html",
        {"measurements": measurements},
    )


def device_list_old(request):
    organization = request.user.profile.organization
    devices = (
        Device.objects
        .filter(organization=organization,deleted_at__isnull=True,)
        .select_related("zone","zone__organization",)
        .order_by("name")
    )
    
    return render(
        request,
        "devices/list.html",
        {
            "devices": devices,
            "organization": organization,
        },
    )
    
# devices/views.py

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render

from .models import Device


ALLOWED_PAGE_SIZES = {5, 15, 30}


def get_scoped_devices(request):
    queryset = (
        Device.objects
        .filter(
            deleted_at__isnull=True,
        )
        .select_related(
            "organization",
            "zone",
        )
        .order_by("name")
    )

    # El superusuario puede ver todo
    if request.user.is_superuser:
        return queryset

    # Usuario normal: solo dispositivos de su organización
    organization = request.user.profile.organization

    return queryset.filter(
        organization=organization
    )


@login_required
def device_list(request):
    # 1. Leer page_size desde la URL
    raw_size = request.GET.get("page_size")
    # 2. Si viene un valor, validarlo
    if raw_size:
        try:
            selected_size = int(raw_size)
        except ValueError:
            selected_size = 15

        # 3. Guardar solamente tamaños permitidos
        if selected_size in ALLOWED_PAGE_SIZES:
            request.session["device_page_size"] = selected_size

    # 4. Recuperar preferencia desde sesión
    page_size = request.session.get(
        "device_page_size",
        15,
    )
    # 5. Obtener dispositivos permitidos para ese usuario
    queryset = get_scoped_devices(request)
    # 6. Paginar
    paginator = Paginator(queryset,page_size,)
    page_obj = paginator.get_page(request.GET.get("page"))
    # 7. Renderizar
    return render(
        request,
        "devices/list.html",
        {
            "page_obj": page_obj,
            "page_size": page_size,
        },
    )
    

def remember_page_size(request):
    request.session["device_page_size"] = 15
    messages.success(
        request,
        "Preferencia de visualización actualizada.",
    )
    return redirect("devices:list")

