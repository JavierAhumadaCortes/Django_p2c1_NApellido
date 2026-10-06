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