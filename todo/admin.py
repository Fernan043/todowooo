from django.contrib import admin
from .models import Todo, Ubicacion, Movimiento
from .models import Proveedor
from .models import OrdenEntrada
from .models import DetalleOrdenEntrada
# Register your models here.

class TodoAdmin(admin.ModelAdmin):
    readonly_fields= ('created',)


#esto hace que cuando ingresamos a admin se vea el objeto añadido en este caso "Todo"
admin.site.register(Todo,TodoAdmin)
admin.site.register(Ubicacion)
admin.site.register(Movimiento)
admin.site.register(Proveedor)
admin.site.register(OrdenEntrada)
admin.site.register(DetalleOrdenEntrada)