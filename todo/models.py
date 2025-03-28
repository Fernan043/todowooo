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

def __str__(self):
    return self.title