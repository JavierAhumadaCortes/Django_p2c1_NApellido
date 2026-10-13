# dashboard/views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render

@login_required
def dashboard(request):
    profile = getattr(request.user, "profile", None)
    if profile is None:
        raise PermissionDenied("La cuenta no posee un perfil habilitado.")

    stats = [
        {'title': 'Ventas', 'value': '$245.890', 'trend': '+12.5%', 'icon': 'bi-currency-dollar', 'bg': 'primary', 'text': 'text-white'},
        {'title': 'Usuarios', 'value': '8.420', 'trend': '+8.2%', 'icon': 'bi-people', 'bg': 'success', 'text': 'text-white'},
        {'title': 'Pedidos', 'value': '1.356', 'trend': '+3.1%', 'icon': 'bi-bag', 'bg': 'warning', 'text': 'text-dark'},
        {'title': 'Retención', 'value': '94.8%', 'trend': '+1.7%', 'icon': 'bi-graph-up-arrow', 'bg': 'danger', 'text': 'text-white'}
    ]

    visits = request.session.get(
        "dashboard_visits",
        0,
    )

    request.session[
        "dashboard_visits"
    ] = visits + 1

    
    return render(
        request,
        "dashboard/index.html",
        {"organization": "", "stats": stats,  "visits": visits + 1,},
    )
    

@login_required
def remember_preference(request):
    request.session[
        "dashboard_mode"
    ] = "compact"

    messages.error(
        request,
        "Preferencia guardada correctamente.",
    )

    return redirect("dashboard:dashboard")


    
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


@login_required
def websocket_page(request):
    return render(
        request,
        "dashboard/test_websocket.html"
    )


@login_required
@require_POST
def test_websocket(request):
    channel_layer = get_channel_layer()

    if channel_layer is None:
        return JsonResponse(
            {"error": "Channel layer no configurado"},
            status=503
        )

    async_to_sync(channel_layer.group_send)(
        "ecoenergy_dashboard",
        {
            "type": "device_event",
            "payload": {
                "type": "device_status_changed",
                "device_id": 999,
                "name": "Sensor de prueba",
                "status": "active",
            },
        },
    )

    return JsonResponse({
        "mensaje": "Evento publicado correctamente"
    })