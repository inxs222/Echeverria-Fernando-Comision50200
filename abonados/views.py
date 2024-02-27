from django.shortcuts import render, redirect
from django.db.models import Sum, Count

from .models import *

from django.http import HttpResponse

from .forms import *

from django.urls import reverse_lazy

from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView

from django.contrib.auth.forms      import AuthenticationForm
from django.contrib.auth            import authenticate, login
from django.contrib.auth.mixins     import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# Funcion para pasar contexto de dashboard

def dashboard():
    debeFacturas = Facturas.objects.filter(pago='False').count()
    totalDeuda = Facturas.objects.filter(pago='False').aggregate(total=Sum('monto'))
    minDeuda = Facturas.objects.filter(pago='False').aggregate(total=Sum('monto') * 0.70)
    totalCobrado = Facturas.objects.filter(pago=True).aggregate(total=Sum('monto'))
    pagasFacturas = Facturas.objects.filter(pago=True).count()
    context = {
        'abonados': Abonado.objects.all(),
        'debeFacturas': debeFacturas,
        'totalDeuda': totalDeuda['total'],
        'minDeuda': round(minDeuda['total'],2),
        'alertasStatus': True,
        'totalCobrado': totalCobrado['total'],
        'pagasFacturas': pagasFacturas
    }
    return context


@login_required
def home(request):
            context = dashboard()
            return render(request, "abonados/home.html", context)

# Servicios
@login_required 
def servicios(request):
    alertasStatus = True
    nAbonado = 14071 
    context = {'servicios': Servicios.objects.all(), 'alertasStatus': alertasStatus, 'nAbonado': nAbonado} 
    return render(request, "abonados/servicios.html", context)

@login_required
def serviciosForm(request):
    if request.method == "POST":
        miForm = AltaServicio(request.POST)
        if miForm.is_valid():
            s_nAbonado = miForm.cleaned_data.get("nAbonado")
            s_servicio = miForm.cleaned_data.get("servicio")
            s_servicioMonto = miForm.cleaned_data.get("servicioMonto")                                       
            servicio = Servicios(nAbonado=s_nAbonado, servicio=s_servicio, servicioMonto=s_servicioMonto)
            servicio.save()
            contexto = dashboard()
            return render(request, "abonados/home.html", contexto)

    else:    
        miForm = AltaServicio()

    return render(request, "abonados/altaServicio.html", {"form": miForm })

@login_required
def buscarServ(request):
    alertasStatus = True
    contexto = {'alertasStatus': alertasStatus}
    return render(request, "abonados/buscarServ.html", contexto)

@login_required
def buscarServicios(request):
    if request.GET["buscar"]:
        alertasStatus = True
        idServicio = request.GET["buscar"]
        servicios = Servicios.objects.filter(servicio__icontains=idServicio)
        mensaje = "Se realizo  correctamente la busqueda de servicios. Valor Buscado: " + idServicio
        contexto = {'servicios': servicios, 'mensaje': mensaje, 'alertasStatus': alertasStatus,}
        return render(request, "abonados/servicios.html", contexto)
    else:
        alertasStatus = True
        mensajeError = "No se ingreso servicio a buscar."
        contexto = {"mensaje": mensajeError, 'alertasStatus': alertasStatus}
        return render(request, "abonados/servicios.html", contexto)

@login_required
def updateServicio(request, idServicio):
    servicio = Servicios.objects.get(id=idServicio)
    if request.method == "POST":
        miForm = AltaServicio(request.POST)
        if miForm.is_valid():
            servicio.nAbonado = miForm.cleaned_data.get('nAbonado')
            servicio.servicio = miForm.cleaned_data.get('servicio') 
            servicio.servicioMonto = miForm.cleaned_data.get('servicioMonto') 
            servicio.save()
            return redirect(reverse_lazy('servicios'))   
    else:
        miForm = AltaServicio(initial={
            'nAbonado': servicio.nAbonado,
            'servicio': servicio.servicio,
            'servicioMonto': servicio.servicioMonto,
        })
    return render(request, "abonados/altaServicio.html", {'form': miForm})

@login_required
def deleteServicio(request, idServicio):
    servicio = Servicios.objects.get(id=idServicio)
    servicio.delete()
    return redirect(reverse_lazy('servicios'))
    
    
# Facturas 
@login_required
def facturas(request):
    alertasStatus = True
    context = {'facturas': Facturas.objects.all(), 'alertasStatus': alertasStatus} 
    return render(request, "abonados/facturas.html", context)

@login_required
def facturasPagas(request):
    alertasStatus = True
    context = {'facturas': Facturas.objects.all(), 'alertasStatus': alertasStatus} 
    return render(request, "abonados/facturaspagas.html", context)

@login_required
def buscarFact(request):
    alertasStatus = True
    contexto = {'alertasStatus': alertasStatus}
    return render(request, "abonados/buscarFact.html", contexto)

@login_required
def buscarFacturas(request):
    if request.GET["buscar"]:
        alertasStatus = True
        factPeriodo = request.GET["buscar"]
        date = Facturas.objects.filter(date__icontains=factPeriodo)
        mensaje = "Se realizo  correctamente la busqueda de Facturas. Periodo Buscado: " + factPeriodo
        contexto = {'facturas': date, 'mensaje': mensaje, 'alertasStatus': alertasStatus }
        return render(request, "abonados/facturas.html", contexto)
    else:
        alertasStatus = True
        mensajeError = "No se ingreso prediodo a buscar."
        contexto = {"mensaje": mensajeError, 'alertasStatus': alertasStatus}
        return render(request, "abonados/facturas.html", contexto)
    
@login_required
def facturasForm(request):
    if request.method == "POST":
        miForm = AltaFacturas(request.POST)
        if miForm.is_valid():
            f_nAbonado = miForm.cleaned_data.get("nAbonado")
            f_nFactura = miForm.cleaned_data.get("nFactura")
            f_monto = miForm.cleaned_data.get("monto")
            f_date = miForm.cleaned_data.get("date")
            f_servicio = miForm.cleaned_data.get("servicio")
            f_pago = miForm.cleaned_data.get("pago")                                                   
            abonados = Facturas(nAbonado=f_nAbonado, nFactura=f_nFactura, monto=f_monto,
                        date=f_date, servicio=f_servicio, pago=f_pago)
            abonados.save()
            contexto = dashboard()
            return render(request, "abonados/home.html", contexto)

    else:    
        miForm = AltaFacturas()

    return render(request, "abonados/altaFacturas.html", {"form": miForm })    

@login_required
def updateFacturas(request, idFacturas):
    facturas = Facturas.objects.get(id=idFacturas)
    if request.method == "POST":
        miForm = AltaFacturas(request.POST)
        if miForm.is_valid():
            facturas.nAbonado = miForm.cleaned_data.get('nAbonado')
            facturas.nFactura = miForm.cleaned_data.get('nFactura') 
            facturas.monto = miForm.cleaned_data.get('monto') 
            facturas.date = miForm.cleaned_data.get('date') 
            facturas.servicio = miForm.cleaned_data.get('servicio')
            facturas.pago = miForm.cleaned_data.get('pago') 
            facturas.save()
            return redirect(reverse_lazy('facturas'))   
    else:
        miForm = AltaFacturas(initial={
            'nAbonado': facturas.nAbonado,
            'nFactura': facturas.nFactura,
            'monto': facturas.monto,
            'date': facturas.date,
            'servicio': facturas.servicio,
            'pago': facturas.monto,
        })
    return render(request, "abonados/altaFacturas.html", {'form': miForm})

@login_required
def deleteFacturas(request, idFacturas):
    servicio = Facturas.objects.get(id=idFacturas)
    servicio.delete()
    return redirect(reverse_lazy('facturas'))

# Abonados
@login_required
def listAbonados(request):
    alertasStatus = True
    context = {'abonados': Abonado.objects.all(), 'alertasStatus': alertasStatus} 
    return render(request, "abonados/listAbonados.html", context)    

@login_required
def abonadosForm(request):
    if request.method == "POST":
        miForm = AltaAbonados(request.POST)
        if miForm.is_valid():
            ab_apellido = miForm.cleaned_data.get("apellido")
            ab_nombre = miForm.cleaned_data.get("nombre")
            ab_direccion = miForm.cleaned_data.get("direccion")
            ab_email = miForm.cleaned_data.get("email")
            ab_nAbonado = miForm.cleaned_data.get("nAbonado")                                                
            abonados = Abonado(apellido=ab_apellido, nombre=ab_nombre, direccion=ab_direccion,
                        email=ab_email, nAbonado=ab_nAbonado)
            abonados.save()
            contexto = dashboard()
            return render(request, "abonados/listAbonados.html", contexto)

    else:    
        miForm = AltaAbonados()

    return render(request, "abonados/altaAbonados.html", {"form": miForm })

@login_required
def buscarAb(request):
    alertasStatus = True
    contexto = {'alertasStatus': alertasStatus}
    return render(request, "abonados/buscarAbonados.html", contexto)

@login_required
def buscarAbonados(request):
    if request.GET["buscar"]:
        alertasStatus = True
        idApellido = request.GET["buscar"]
        abonados = Abonado.objects.filter(apellido__icontains=idApellido)
        mensaje = "Se realizo  correctamente la busqueda. Valor Buscado: " + idApellido
        contexto = {'abonados': abonados, 'mensaje': mensaje, 'alertasStatus': alertasStatus}
        return render(request, "abonados/listAbonados.html", contexto)
    else:
        alertasStatus = True
        mensajeError = "No se ingreso servicio a buscar."
        contexto = {"mensaje": mensajeError, 'alertasStatus': alertasStatus}
        return render(request, "abonados/listAbonados.html", contexto)
    
@login_required
def updateAbonados(request, idAbonados):
    abonados = Abonado.objects.get(id=idAbonados)
    if request.method == "POST":
        miForm = AltaAbonados(request.POST)
        if miForm.is_valid():
            abonados.apellido = miForm.cleaned_data.get('apellido')
            abonados.nombre = miForm.cleaned_data.get('nombre') 
            abonados.direccion = miForm.cleaned_data.get('direccion')
            abonados.email = miForm.cleaned_data.get('email') 
            abonados.nAbonado = miForm.cleaned_data.get('nAbonado') 
            abonados.save()
            return redirect(reverse_lazy('listAbonados'))   
    else:
        miForm = AltaAbonados(initial={
            'apellido': abonados.apellido,
            'nombre': abonados.nombre,
            'direccion': abonados.direccion,
            'email': abonados.email,
            'nAbonado': abonados.nAbonado,
        })
    return render(request, "abonados/altaAbonados.html", {'form': miForm})

@login_required
def deleteAbonados(request, idAbonados):
    abonados = Abonado.objects.get(id=idAbonados)
    abonados.delete()
    return redirect(reverse_lazy('listAbonados'))

# Tickets

@login_required
def tickets(request):
    context = {'tickets': Tickets.objects.all()} 
    return render(request, "abonados/tickets.html", context)

@login_required
def ticketsForm(request):
    if request.method == "POST":
        miForm = AltaTickets(request.POST)
        if miForm.is_valid():
            t_nTicket = miForm.cleaned_data.get("nTicket")
            t_fecha = miForm.cleaned_data.get("fecha")
            t_descrip = miForm.cleaned_data.get("descrip")
            t_nAbonado = miForm.cleaned_data.get("nAbonado")   
            t_estado = miForm.cleaned_data.get("estado")                                             
            tickets = Tickets(nTicket=t_nTicket, fecha=t_fecha, descrip=t_descrip,
                        estado=t_estado, nAbonado=t_nAbonado)
            tickets.save()
            contexto = {'tickets': Tickets.objects.all()}
            return render(request, "abonados/tickets.html", contexto)

    else:    
        miForm = AltaTickets()

    return render(request, "abonados/altaTickets.html", {"form": miForm })

@login_required
def updateTicket(request, idTicket):
    ticket = Tickets.objects.get(id=idTicket)
    if request.method == "POST":
        miForm = AltaTickets(request.POST)
        if miForm.is_valid():
            ticket.nTicket = miForm.cleaned_data.get('nTicket')
            ticket.fecha = miForm.cleaned_data.get('fecha') 
            ticket.descrip = miForm.cleaned_data.get('descrip')
            ticket.nAbonado = miForm.cleaned_data.get('nAbonado') 
            ticket.estado = miForm.cleaned_data.get('estado') 
            ticket.save()
            return redirect(reverse_lazy('tickets'))   
    else:
        miForm = AltaTickets(initial={
        'nTicket': ticket.nTicket,
        'fecha': ticket.fecha,
        'descrip': ticket.descrip,
        'nAbonado': ticket.nAbonado,
        'estado': ticket.estado,
        })
    return render(request, "abonados/altaTickets.html", {'form': miForm})

@login_required
def deleteTicket(request, idTicket):
    tickets = Tickets.objects.get(id=idTicket)
    tickets.delete()
    return redirect(reverse_lazy('tickets'))

@login_required
def buscarT(request):
    alertasStatus = True
    contexto = {'alertasStatus': alertasStatus}
    return render(request, "abonados/buscarTicket.html", contexto)

@login_required
def buscarTicket(request):
    if request.GET["buscar"]:
        alertasStatus = True
        idTicket = request.GET["buscar"]
        idTicket_int = int(idTicket)
        tickets = Tickets.objects.filter(nTicket=idTicket_int)
        mensaje = "Se realizo  correctamente la busqueda. Valor Buscado: " + idTicket
        contexto = {'tickets': tickets, 'mensaje': mensaje, 'alertasStatus': alertasStatus}
        return render(request, "abonados/tickets.html", contexto)
    else:
        alertasStatus = True
        mensajeError = "No se ingreso servicio a buscar."
        contexto = {"mensaje": mensajeError, 'alertasStatus': alertasStatus}
        return render(request, "abonados/tickets.html", contexto)    

# Login Register Autenthicate

def login_request(request):
    if request.method == "POST":
        usuario = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=usuario, password=password)
        if user is not None:
            login(request, user)
            contexto = dashboard()
            #____ Avatar
            try:
                avatar = Avatar.objects.get(user=request.user.id).imagen.url
            except:
                avatar = "/media/avatares/default.png"
            finally:
                request.session["avatar"] = avatar
            #__________________________________________
            return render(request, "abonados/home.html", contexto)
        else:
            miForm = AuthenticationForm(request, data=request.POST)
            return render(request, "abonados/login.html", {"form": miForm })
        
    miForm = AuthenticationForm()
    return render(request, "abonados/login.html", {"form": miForm })       

def register(request):
    if request.method == "POST":
        miForm = RegistroForm(request.POST)
        if miForm.is_valid():
            usuario = miForm.cleaned_data.get("username")
            miForm.save()
            return redirect(reverse_lazy('login'))

    else:    
        miForm = RegistroForm()

    return render(request, "abonados/registro.html", {"form": miForm })  
    

@login_required
def editUser(request):
    usuario = request.user
    if request.method == "POST":
        form = UserEditForm(request.POST, instance = usuario)
        if form.is_valid():
            informacion = form.cleaned_data
            user = User.objects.get(username=usuario)
            user.email = informacion['email']
            user.first_name = informacion['first_name']
            user.last_name = informacion['last_name']
            user.set_password(informacion['password1'])
            user.save()
            return render(request, "abonados/home.html")
    else:    
        form = UserEditForm(instance=usuario)

    return render(request, "abonados/editarPerfil.html", {"form": form }) 



@login_required
def agregarAvatar(request):
    if request.method == "POST":
        form = AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            usuario = User.objects.get(username=request.user)

            # ____ Para borrar el avatar viejo
            avatarViejo = Avatar.objects.filter(user=usuario)
            if len(avatarViejo) > 0:
                for i in range(len(avatarViejo)):
                    avatarViejo[i].delete()
            # __________________________________
            avatar = Avatar(user=usuario, imagen=form.cleaned_data['imagen'])
            avatar.save()

            # ___________ Hago una url de la imagen en request
            imagen = Avatar.objects.get(user=request.user.id).imagen.url
            request.session["avatar"] = imagen
            contexto = dashboard()
            return render(request, "abonados/home.html", contexto)

    else:    
        form = AvatarForm()

    return render(request, "abonados/agregarAvatar.html", {"form": form })  


def acerca(request):
    return render(request, "abonados/acerca.html")  