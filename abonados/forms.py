from django import forms   
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class AltaAbonados(forms.Form):
    apellido = forms.CharField(max_length=50)
    nombre = forms.CharField(max_length=50)
    direccion = forms.CharField(max_length=50)
    email = forms.EmailField()
    nAbonado = forms.IntegerField()


class AltaServicio(forms.Form):
    nAbonado = forms.IntegerField()
    servicio = forms.CharField(max_length=250)
    servicioMonto = forms.IntegerField()


class AltaFacturas(forms.Form):
    nAbonado = forms.IntegerField()
    nFactura = forms.IntegerField()
    monto = forms.IntegerField()
    date = forms.DateTimeField()
    servicio = forms.CharField(max_length=50)
    pago = forms.BooleanField(required=False)
    
class AltaTickets(forms.Form):
    nTicket = forms.IntegerField() 
    fecha = forms.DateField()
    descrip = forms.CharField(max_length=200)
    nAbonado = forms.IntegerField() 
    estado = forms.BooleanField(required=False)
    
class RegistroForm(UserCreationForm):
    email = forms.EmailField(max_length=50, required=True)
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar Contraseña", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
class UserEditForm(UserCreationForm):
    email = forms.EmailField(max_length=50, required=True)
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar Contraseña", widget=forms.PasswordInput)
    first_name = forms.CharField(label="Nombre/s", max_length=50, required=True)
    last_name = forms.CharField(label="Apellido/s", max_length=50, required=True)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name']
        
class AvatarForm(forms.Form):
    imagen = forms.ImageField(required=True)