from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Abonado(models.Model):
    apellido = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    email = models.EmailField()
    nAbonado = models.IntegerField()

    def __str__(self):
        return f"{self.nAbonado}, {self.apellido.upper()}, {self.nombre.upper()}"

class Facturas(models.Model):
    nAbonado = models.IntegerField()
    nFactura = models.IntegerField()
    monto = models.IntegerField()
    date = models.DateTimeField()
    servicio = models.CharField(max_length=50)
    pago = models.BooleanField()

    def __str__(self):
        return f"N_Abonado {self.nAbonado}, N_Factura {self.nFactura}, Monto {self.monto} , Fecha {self.date}"
    
    
class Servicios(models.Model):
    nAbonado = models.IntegerField()
    servicio = models.CharField(max_length=250)
    servicioMonto = models.IntegerField()
    
    def __str__(self):
        return f"N_Abonado {self.nAbonado} Servicio {self.servicio}  Monto {self.servicioMonto}"
    
class Tickets(models.Model):
    nTicket = models.IntegerField() 
    fecha = models.DateField()
    descrip = models.CharField(max_length=200)
    nAbonado = models.IntegerField()
    estado = models.BooleanField()
    
    def __str__(self):
        return f"N_Ticket {self.nTicket} Fecha {self.fecha}  Estado {self.estado}"

class Avatar(models.Model):
    imagen = models.ImageField(upload_to="avatares")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} {self.imagen}"   