from django.db import models
from django.contrib.auth.models import User



# el import de User basicamente se utiliza como clave forenea para unir dos modelos
# en SQL seria el igual de una clave foranea entre tablas
#la variable user funciona de esa menera para realizar la conexion
#cada usuario en django por defecto tienen un id la cual actua como una id de SQL
#Investigar mas para el proyecto

class Todo(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add = True)
    datecompleted = models.DateTimeField(null = True, blank=True)
    important = models.BooleanField(default = False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    ubicacion = models.ForeignKey('Ubicacion', on_delete=models.SET_NULL, null=True, blank=True)


class Ubicacion(models.Model):
    pasillo = models.CharField(max_length=10)
    estante = models.CharField(max_length=10)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return f"P{self.pasillo}-E{self.estante}"

class Movimiento(models.Model):
    TIPOS_MOVIMIENTO = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
    ]

    producto = models.ForeignKey(Todo, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPOS_MOVIMIENTO)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.producto.title} ({self.cantidad})"

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    correo = models.EmailField(blank=True)

    def __str__(self):
        return self.nombre


class OrdenEntrada(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    fecha_orden = models.DateField(auto_now_add=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return f"Orden #{self.id} - {self.proveedor.nombre}"

class DetalleOrdenEntrada(models.Model):
    orden = models.ForeignKey(OrdenEntrada, on_delete=models.CASCADE)
    producto = models.ForeignKey(Todo, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.producto.title} x{self.cantidad} en Orden #{self.orden.id}"

def __str__(self):
    return self.title