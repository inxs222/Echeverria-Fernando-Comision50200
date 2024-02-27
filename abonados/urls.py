from django.urls import path, include
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', home, name="home"),

    path('servicios/', servicios, name="servicios"),
    path('updateServicio/<idServicio>/', updateServicio, name="updateServicio"),
    path('servicio_borrar/<idServicio>/', deleteServicio, name="servicioBorrar"),
    path('buscarServ/', buscarServ, name="buscarServ"),
    path('buscarServicios/', buscarServicios, name="buscarServicios"),
    path('altaServicio', serviciosForm, name="altaServicio"),
    
    path('facturas/', facturas, name="facturas"),
    path('facturaspagas/', facturasPagas, name="facturasPagas"),    
    path('buscarFact/', buscarFact, name="buscarFact"),
    path('buscarFacturas/', buscarFacturas, name="buscarFacturas"),
    path('altaFacturas/', facturasForm, name="altaFacturas"),
    path('updateFacturas/<idFacturas>/', updateFacturas, name="updateFacturas"),
    path('facturasBorrar/<idFacturas>/', deleteFacturas, name="facturasBorrar"),
    
    path('altaAbonados/', abonadosForm, name="altaAbonados"),
    path('listAbonados/', listAbonados, name="listAbonados"),
    path('buscarAbonados/', buscarAbonados, name="buscarAbonados"),
    path('buscarAb/', buscarAb, name="buscarAb"),
    path('updateAbonados/<idAbonados>/', updateAbonados, name="updateAbonados"),
    path('abonadosBorrar/<idAbonados>/', deleteAbonados, name="abonadosBorrar"),
    
    path("tickets", tickets, name="tickets"),
    path("altaTickets", ticketsForm, name="altaTickets"),
    path('updateTicket/<idTicket>/', updateTicket, name="updateTicket"),
    path('ticketBorrar/<idTicket>/', deleteTicket, name="ticketBorrar"),
    path('buscarTicket/', buscarTicket, name="buscarTicket"),
    path('buscarT/', buscarT, name="buscarT"),
    
    path('login/', login_request, name="login"),
    path('registro/', register, name="registro"),
    path('logout/', LogoutView.as_view(template_name="abonados/logout.html"), name="logout"),
    path('editUser/', editUser, name="editUser"),
    path('agregar_avatar/', agregarAvatar, name="agregar_avatar"),

    path('acerca/', acerca, name="acerca"),

]